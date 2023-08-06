#
# Copyright 2018-2020 Florian Dematraz <florian.dematraz@snoozeweb.net>
# Copyright 2018-2020 Guillaume Ludinard <guillaume.ludi@gmail.com>
# Copyright 2020-2021 Japannext Co., Ltd. <https://www.japannext.co.jp/>
# SPDX-License-Identifier: AFL-3.0
#

'''Module for handling the falcon WSGI'''

import os
import functools
from logging import getLogger
from hashlib import sha256
from base64 import b64decode
from abc import abstractmethod

from dataclasses import asdict

import bson.json_util
import falcon
from falcon_auth import FalconAuthMiddleware, BasicAuthBackend, JWTAuthBackend
from falcon.errors import HTTPInternalServerError
from wsgiref.simple_server import make_server, WSGIServer
from socketserver import ThreadingMixIn
from ldap3 import Server, Connection, ALL, SUBTREE
from ldap3.core.exceptions import LDAPOperationResult, LDAPExceptionError

from snooze.api.base import BasicRoute
from snooze.api.static import StaticRoute
from snooze.utils import config, write_config
from snooze.utils.functions import ensure_kv
from snooze.health import HealthRoute

log = getLogger('snooze.api')

class LoggerMiddleware(object):
    '''Middleware for logging'''

    def __init__(self, conf=None):
        if conf is None:
            conf = {}
        self.logger = getLogger('snooze.audit')
        self.excluded_paths = conf.get('audit_excluded_paths', [])

    def process_response(self, req, resp, *_args):
        '''Method for handling requests as a middleware'''
        source = req.access_route[0]
        method = req.method
        path = req.relative_uri
        status = resp.status[:3]
        message = f"{source} {method} {path} {status}"
        if not any(path.startswith(excluded) for excluded in self.excluded_paths):
            self.logger.debug(message)


class ThreadingWSGIServer(ThreadingMixIn, WSGIServer):
    '''Daemonized threaded WSGI server'''
    daemon_threads = True

def authorize(func):
    '''Decorator for methods that are protected by authorization'''
    def _f(self, req, resp, *args, **kw):
        if os.environ.get('SNOOZE_NO_LOGIN', self.core.conf.get('no_login', False)):
            return func(self, req, resp, *args, **kw)
        user_payload = req.context['user']['user']
        if (self.plugin and hasattr(self.plugin, 'name')):
            plugin_name = self.plugin.name
        elif self.name:
            plugin_name = self.name
        if plugin_name:
            read_permissions = ['ro_all', 'rw_all', 'ro_'+plugin_name, 'rw_'+plugin_name]
            write_permissions = ['rw_all', 'rw_'+plugin_name]
        else:
            plugin_name = 'unknown'
            read_permissions = ['ro_all', 'rw_all']
            write_permissions = ['rw_all']
        endpoint = func.__name__
        method = user_payload['method']
        name = user_payload['name']
        if name == 'root' and method == 'root':
            log.warning("Root user detected! Authorized but please use a proper admin role if possible (authorization '{}' for plugin {})".format(endpoint, plugin_name))
            return func(self, req, resp, *args, **kw)
        else:
            permissions = user_payload.get('permissions', [])
            permissions.append('any')
            if endpoint == 'on_get':
                if self.authorization_policy and any(perm in permissions for perm in self.authorization_policy.get('read', [])):
                    return func(self, req, resp, *args, **kw)
                elif any(perm in permissions for perm in read_permissions):
                    return func(self, req, resp, *args, **kw)
            elif endpoint in ['on_post', 'on_put', 'on_delete']:
                if self.check_permissions:
                    permissions = self.get_permissions(self.get_roles(name, method))
                if len(permissions) > 0:
                    if self.authorization_policy and any(perm in permissions for perm in self.authorization_policy.get('write', [])):
                        return func(self, req, resp, *args, **kw)
                    elif any(perm in permissions for perm in write_permissions):
                        return func(self, req, resp, *args, **kw)
        log.warning("Access denied. User %s on endpoint '%s' for plugin %s", name, endpoint, plugin_name)
        raise falcon.HTTPForbidden('Forbidden', 'Permission Denied')
    return _f

class FalconRoute(BasicRoute):
    '''Basic falcon route'''
    def inject_payload_media(self, req, resp):
        user_payload = req.context['user']['user']
        log.debug("Injecting payload %s to %s", user_payload, req.media)
        if isinstance(req.media, list):
            for media in req.media:
                media['name'] = user_payload['name']
                media['method'] = user_payload['method']
        else:
            req.media['name'] = user_payload['name']
            req.media['method'] = user_payload['method']

    def inject_payload_search(self, req, s):
        user_payload = req.context['user']['user']
        to_inject = ['AND', ['=', 'name', user_payload['name']], ['=', 'method', user_payload['method']]]
        if s:
            return ['AND', s, to_inject]
        else:
            return to_inject

    def update_password(self, media):
        password = media.pop('password', None)
        name = media.get('name')
        method = media.get('method')
        if not password or not name or method != 'local':
            log.debug("Skipping updating password")
            return
        log.debug("Updating password for %s user %s", method, name)
        user_password = {}
        user_password['name'] = name
        user_password['method'] = method
        user_password['password'] = sha256(password.encode('utf-8')).hexdigest()
        self.core.db.write('user.password', user_password, 'name,method')

def merge_batch_results(rec_list):
    '''Merge the results (added/rejected/...) in the case of a batch'''
    return {'data': functools.reduce(lambda a, b: {k: a.get('data', {}).get(k, []) + b.get('data', {}).get(k, []) for k in list(dict.fromkeys(list(a.get('data', {}).keys()) + list(b.get('data', {}).keys())))}, rec_list)}

class WebhookRoute(FalconRoute):
    auth = {
        'auth_disabled': True
    }

    @abstractmethod
    def parse_webhook(self, req, media):
        pass

    def on_post(self, req, resp):
        log.debug("Received webhook log %s", req.media)
        media = req.media.copy()
        rec_list = [{'data': {}}]
        if not isinstance(media, list):
            media = [media]
        for req_media in media:
            try:
                alerts = self.parse_webhook(req, req_media)
                if alerts:
                    if not isinstance(alerts, list):
                        alerts = [alerts]
                    for alert in alerts:
                        for key, val in req.params.items():
                            alert = ensure_kv(alert, val, *key.split('.'))
                        rec = self.core.process_record(alert)
                        rec_list.append(rec)
            except Exception as e:
                log.exception(e)
                rec_list.append({'data': {'rejected': [req_media]}})
                continue
        resp.content_type = falcon.MEDIA_JSON
        resp.status = falcon.HTTP_200
        resp.media = merge_batch_results(rec_list)

class PermissionsRoute(BasicRoute):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = 'role'

    @authorize
    def on_get(self, req, resp):
        log.debug("Listing permissions")
        try:
            permissions = ['rw_all', 'ro_all']
            for plugin in self.api.core.plugins:
                permissions.append('rw_' + plugin.name)
                permissions.append('ro_' + plugin.name)
                for additional_permission in plugin.permissions:
                    permissions.append(additional_permission)
            log.debug("List of permissions: {}".format(permissions))
            resp.content_type = falcon.MEDIA_JSON
            resp.status = falcon.HTTP_200
            resp.media = {
                'data': permissions,
            }
        except Exception as e:
            log.exception(e)
            resp.status = falcon.HTTP_503

class AlertRoute(BasicRoute):
    auth = {
        'auth_disabled': True
    }

    def on_post(self, req, resp):
        log.debug("Received log %s", req.media)
        media = req.media.copy()
        rec_list = [{'data': {}}]
        if not isinstance(media, list):
            media = [media]
        for req_media in media:
            try:
                rec = self.core.process_record(req_media)
                rec_list.append(rec)
            except Exception as e:
                log.exception(e)
                rec_list.append({'data': {'rejected': [req_media]}})
                continue
        resp.content_type = falcon.MEDIA_JSON
        resp.status = falcon.HTTP_200
        resp.media = merge_batch_results(rec_list)

class MetricsRoute(BasicRoute):
    '''A falcon route to serve prometheus metrics'''
    auth = {
        'auth_disabled': True
    }

    def on_get(self, req, resp):
        try:
            resp.content_type = falcon.MEDIA_TEXT
            data = self.api.core.stats.get_metrics()
            resp.body = str(data.decode('utf-8'))
            resp.status = falcon.HTTP_200
        except Exception as err:
            log.exception(err)
            resp.status = falcon.HTTP_503

class LoginRoute(BasicRoute):
    '''A falcon route for users to login'''
    auth = {
        'auth_disabled': True
    }

    def on_get(self, req, resp):
        log.debug("Listing authentication backends")
        if os.environ.get('SNOOZE_NO_LOGIN', self.core.conf.get('no_login', False)):
            resp.content_type = falcon.MEDIA_JSON
            resp.status = falcon.HTTP_200
            resp.media = {
                'token': self.api.get_root_token(),
            }
            return
        try:
            backends = [
                {'name':self.api.auth_routes[backend].name, 'endpoint': backend}
                for backend in self.api.auth_routes.keys()
                if self.api.auth_routes[backend].enabled
            ]
            resp.content_type = falcon.MEDIA_JSON
            resp.status = falcon.HTTP_200
            default_auth_backend = self.api.core.general_conf.get('default_auth_backend', '')
            default_backends = [x for x in backends if x['endpoint'] == default_auth_backend]
            if len(default_backends) > 0:
                backends.remove(default_backends[0])
                backends.insert(0, default_backends[0])
            resp.media = {
                'data': {'backends': backends},
            }
        except Exception as err:
            log.exception(err)
            resp.status = falcon.HTTP_503

class ReloadRoute(BasicRoute):
    '''A falcon route to reload one's token'''
    auth = {
        'auth_disabled': True
    }

    def on_post(self, req, resp):
        media = req.media.copy()
        if media.get('reload_token', '-') == self.api.core.secrets.get('reload_token', '+'):
            filename = media.get('filename')
            conf = media.get('conf')
            _reload = media.get('reload')
            sync = media.get('sync', False)
            log.debug("Reloading conf (%s, %s), backend %s, sync %s", filename, conf, _reload, sync)
            results = self.api.write_and_reload(filename, conf, _reload, sync)
            resp.content_type = falcon.MEDIA_TEXT
            resp.status = results.get('status', falcon.HTTP_503)
            resp.text = results.get('text', '')
        else:
            resp.status = falcon.HTTP_401
            resp.text = 'Invalid secret reload token'

class ClusterRoute(BasicRoute):
    auth = {
        'auth_disabled': True
    }

    def on_get(self, req, resp):
        log.debug("Listing cluster members")
        cluster = self.core.threads['cluster']
        if req.params.get('self', False):
            members = [cluster.status()]
        else:
            members = cluster.members_status()
        resp.content_type = falcon.MEDIA_JSON
        resp.status = falcon.HTTP_200
        resp.media = {
            'data': [asdict(m) for m in members],
        }

class CORS:
    '''A falcon middleware to handle CORS when the snooze-server and
    snooze-web components are on different hosts.
    '''
    def __init__(self):
        pass

    def process_response(self, req, resp, _resource, req_succeeded):
        resp.set_header('Access-Control-Allow-Origin', '*')
        if (
            req_succeeded
            and req.method == 'OPTIONS'
            and req.get_header('Access-Control-Request-Method')
        ):
            allow = resp.get_header('Allow')
            resp.delete_header('Allow')

            allow_headers = req.get_header('Access-Control-Request-Headers', default='*')
            resp.set_headers(
                (
                    ('Access-Control-Allow-Methods', allow),
                    ('Access-Control-Allow-Headers', allow_headers),
                    ('Access-Control-Max-Age', '86400'),  # 24 hours
                )
            )

class AuthRoute(BasicRoute):
    auth = {
        'auth_disabled': True
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.auth_header_prefix = 'Basic'
        self.userplugin = self.api.core.get_core_plugin('user')
        self.enabled = True

    def parse_auth_token_from_request(self, auth_header):
        """
        Parses and returns Auth token from the request header. Raises
        `falcon.HTTPUnauthoried exception` with proper error message
        """
        if not auth_header:
            raise falcon.HTTPUnauthorized(
                description='Missing Authorization Header')

        parts = auth_header.split()

        if parts[0].lower() != self.auth_header_prefix.lower():
            raise falcon.HTTPUnauthorized(
                description=f"Invalid Authorization Header: Must start with {self.auth_header_prefix}")

        elif len(parts) == 1:
            raise falcon.HTTPUnauthorized(
                description='Invalid Authorization Header: Token Missing')
        elif len(parts) > 2:
            raise falcon.HTTPUnauthorized(
                description='Invalid Authorization Header: Contains extra content')

        return parts[1]

    def _extract_credentials(self, req):
        auth = req.get_header('Authorization')
        token = self.parse_auth_token_from_request(auth_header=auth)
        try:
            token = b64decode(token).decode('utf-8')

        except Exception:
            raise falcon.HTTPUnauthorized(
                description='Invalid Authorization Header: Unable to decode credentials')

        try:
            username, password = token.split(':', 1)
        except ValueError:
            raise falcon.HTTPUnauthorized(
                description='Invalid Authorization: Unable to decode credentials')

        return username, password

    def parse_user(self, user):
        return user

    def inject_permissions(self, user):
        roles = self.get_roles(user['name'], user['method'])
        permissions = self.get_permissions(roles)
        user['roles'] = roles
        user['permissions'] = permissions

    def on_post(self, req, resp):
        if self.enabled:
            self.authenticate(req, resp)
            user = self.parse_user(req.context['user'])
            preferences = None
            if self.userplugin:
                _, preferences = self.userplugin.manage_db(user)
            self.inject_permissions(user)
            log.debug("Context user: %s", user)
            token = self.api.jwt_auth.get_auth_token(user)
            log.debug("Generated token: %s", token)
            resp.content_type = falcon.MEDIA_JSON
            resp.status = falcon.HTTP_200
            resp.media = {
                'token': token,
            }
            if preferences:
                resp.media['default_page'] = preferences.get('default_page')
        else:
            resp.content_type = falcon.MEDIA_JSON
            resp.status = falcon.HTTP_409
            resp.media = {
                'response': 'Backend disabled',
            }

    @abstractmethod
    def authenticate(self, req, resp):
        '''Abstract method called to authenticate the user.
        Is expected to set req.context['user'], and to raise
        falcon.HTTPUnauthorized when unauthorized.
        '''

    @abstractmethod
    def reload(self):
        '''Abstract method to reload the configuration. Usually make
        use of snooze.utils.config to do so.'''

class AnonymousAuthRoute(AuthRoute):
    '''An authentication route for anonymous users'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = 'Anonymous'
        self.reload()

    def reload(self):
        conf = config('general')
        self.enabled = conf.get('anonymous_enabled', False)
        log.debug("Authentication backend 'anonymous' status: %s", self.enabled)

    def authenticate(self, req, resp):
        log.debug('Anonymous login')
        req.context['user'] = 'anonymous'

    def parse_user(self, user):
        return {'name': 'anonymous', 'method': 'local'}

class LocalAuthRoute(AuthRoute):
    '''An authentication route for local users'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = 'Local'
        self.reload()

    def reload(self):
        conf = config('general')
        self.enabled = conf.get('local_users_enabled', False)
        log.debug("Authentication backend 'local' status: %s", self.enabled)

    def authenticate(self, req, resp):
        username, password = self._extract_credentials(req)
        password_hash = sha256(password.encode('utf-8')).hexdigest()
        log.debug("Attempting login for %s, with password hash %s", username, password_hash)
        user_search = self.core.db.search('user', ['AND', ['=', 'name', username], ['=', 'method', 'local']])
        try:
            if user_search['count'] > 0:
                query = ['AND', ['=', 'name', username], ['=', 'method', 'local']]
                db_password_search = self.core.db.search('user.password', query)
                try:
                    db_password = db_password_search['data'][0]['password']
                except Exception as _err:
                    raise falcon.HTTPUnauthorized(
                		description='Password not found')
                if db_password == password_hash:
                    log.debug('Password was correct for user %s', username)
                    req.context['user'] = username
                else:
                    log.debug('Password was incorrect for user %s', username)
                    raise falcon.HTTPUnauthorized(
                		description='Invalid Username/Password')
            else:
                log.debug('User %s does not exist', username)
                raise falcon.HTTPUnauthorized(
                	description='User does not exist')
        except Exception as e:
            log.exception('Exception while trying to compare passwords')
            raise falcon.HTTPUnauthorized(
           		description='Exception while trying to compare passwords')

    def parse_user(self, user):
        return {'name': user, 'method': 'local'}

class LdapAuthRoute(AuthRoute):
    '''An authentication route for LDAP users'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = 'Ldap'
        self.reload()

    def reload(self):
        conf = config('ldap_auth')
        self.enabled = conf.get('enabled') or False
        if self.enabled:
            try:
                self.base_dn = conf['base_dn']
                self.group_dn = conf.get('group_dn', self.base_dn)
                self.user_filter = conf['user_filter']
                self.email_attribute = conf.get('email_attribute') or 'mail'
                self.display_name_attribute = conf.get('display_name_attribute') or 'cn'
                self.member_attribute = conf.get('member_attribute') or 'memberof'
                self.auth_header_prefix = conf.get('auth_header_prefix') or 'Basic'
                self.bind_dn = conf['bind_dn']
                self.bind_password = conf['bind_password']
                self.port = conf.get('port') or ''
                self.host = conf['host']
                if not self.host.startswith('ldap://') and not self.host.startswith('ldaps://'):
                    if str(self.port) == '636':
                        self.host = 'ldaps://' + self.host
                    else:
                        self.host = 'ldap://' + self.host
                if self.port:
                    self.server = Server(self.host, port=self.port, get_info=ALL, connect_timeout=10)
                else:
                    self.server = Server(self.host, get_info=ALL, connect_timeout=10)
                bind_con = Connection(
                    self.server,
                    user=self.bind_dn,
                    password=self.bind_password,
                    raise_exceptions=True
                )
                if not bind_con.bind():
                    log.error("Cannot BIND to LDAP server: %s:%s", conf['host'], conf['port'])
                    self.enabled = False
            except Exception as err:
                log.exception(err)
                self.enabled = False
        log.debug("Authentication backend 'ldap'. Enabled: %s", self.enabled)

    def _search_user(self, username):
        try:
            bind_con = Connection(
                self.server,
                user=self.bind_dn,
                password=self.bind_password,
                raise_exceptions=True
            )
            bind_con.bind()
            user_filter = self.user_filter.replace('%s', username)
            bind_con.search(
                search_base = self.base_dn,
                search_filter = user_filter,
                attributes = [self.display_name_attribute, self.email_attribute, self.member_attribute],
                search_scope = SUBTREE
            )
            response = bind_con.response
            if (
                bind_con.result['result'] == 0
                and len(response) > 0
                and 'dn' in response[0].keys()
            ):
                user_dn = response[0]['dn']
                attributes = response[0]['attributes']
                groups = [
                    group for group in attributes[self.member_attribute]
                    for dn in self.group_dn.split(':')
                    if group.endswith(dn)
                ]
                return {'name': username, 'dn': user_dn, 'groups': groups}
            else:
                # Could not find user in search
                raise falcon.HTTPUnauthorized(description=f"Error in search: Could not find user {username} in LDAP search")
        except LDAPOperationResult as err:
            raise falcon.HTTPUnauthorized(description=f"Error during search: {err}")
        except LDAPExceptionError as err:
            raise falcon.HTTPUnauthorized(description=f"Error during search: {err}")

    def _bind_user(self, user_dn, password):
        try:
            user_con = Connection(
                self.server,
                user=user_dn,
                password=password,
                raise_exceptions=True
            )
            user_con.bind()
            return user_con
        except LDAPOperationResult as err:
            raise falcon.HTTPUnauthorized(description=f"Error during bind: {err}")
        except LDAPExceptionError as err:
            raise falcon.HTTPUnauthorized(description=f"Error during bind: {err}")
        finally:
            user_con.unbind()

    def authenticate(self, req, resp):
        username, password = self._extract_credentials(req)
        user = self._search_user(username)
        user_con = self._bind_user(user['dn'], password)
        if user_con.result['result'] == 0:
            req.context['user'] = user
        else:
            raise falcon.HTTPUnauthorized(description="")

    def parse_user(self, user):
        groups = list(map(lambda x: x.split(',')[0].split('=')[1], user['groups']))
        return {'name': user['name'], 'groups': groups, 'method': 'ldap'}

class RedirectRoute:
    '''A falcon route for managing the default redirection'''
    auth = {
        'auth_disabled': True
    }
    def on_get(self, req, resp):
        raise falcon.HTTPMovedPermanently('/web/')

SNOOZE_GLOBAL_RUNDIR = '/var/run/snooze'
uid = os.getuid()
SNOOZE_LOCAL_RUNDIR = f"/var/run/user/{uid}"

class BackendApi():
    def init_api(self, core):
        # Authentication
        self.core = core
        self.cluster = core.threads['cluster']

        # JWT setup
        self.secret = '' if os.environ.get('SNOOZE_NO_LOGIN', self.core.conf.get('no_login', False)) else self.core.secrets['jwt_private_key']
        def auth(payload):
            log.debug("Payload received: %s", payload.get('user', {}).get('name', payload))
            return payload
        self.jwt_auth = JWTAuthBackend(auth, self.secret)

        # Handler
        self.handler = falcon.API(middleware=[CORS(), LoggerMiddleware(self.core.conf), FalconAuthMiddleware(self.jwt_auth)])
        self.handler.req_options.auto_parse_qs_csv = False

        json_handler = falcon.media.JSONHandler(
            dumps=bson.json_util.dumps,
            loads=bson.json_util.loads,
        )
        self.handler.req_options.media_handlers.update({'application/json': json_handler})
        self.handler.resp_options.media_handlers.update({'application/json': json_handler})
        self.handler.add_error_handler(Exception, self.custom_handle_uncaught_exception)
        self.auth_routes = {}
        # Alert route
        self.add_route('/alert', AlertRoute(self))
        # List route
        self.add_route('/login', LoginRoute(self))
        # Reload route
        self.add_route('/reload', ReloadRoute(self))
        # Cluster route
        self.add_route('/cluster', ClusterRoute(self))
        # Health route
        self.add_route('/health', HealthRoute(self))
        # Permissions route
        self.add_route('/permissions', PermissionsRoute(self))
        # Basic auth setup
        self.auth_routes['local'] = LocalAuthRoute(self)
        self.add_route('/login/local', self.auth_routes['local'])
        # Anonymous auth
        if self.core.general_conf.get('anonymous_enabled', False):
            self.auth_routes['anonymous'] = AnonymousAuthRoute(self)
            self.add_route('/login/anonymous', self.auth_routes['anonymous'])
        # Ldap auth
        self.auth_routes['ldap'] = LdapAuthRoute(self)
        self.add_route('/login/ldap', self.auth_routes['ldap'])
        # Optional metrics
        if self.core.stats.enabled:
            self.add_route('/metrics', MetricsRoute(self), '')

        web_conf = self.core.conf.get('web', {})
        if web_conf.get('enabled', True):
            self.add_route('/', RedirectRoute(), '')
            self.add_route('/web', RedirectRoute(), '')
            self.handler.add_sink(StaticRoute(web_conf.get('path', '/opt/snooze/web'), '/web').on_get, '/web')

    def custom_handle_uncaught_exception(self, e, req, resp, params):
        '''Custom handler for logging uncaught exceptions in falcon inside python logger.
        Make use of an internal method of falcon to do so.
        '''
        log.exception(e)
        self.handler._compose_error_response(req, resp, HTTPInternalServerError())

    def add_route(self, route, action, prefix='/api'):
        '''Map a falcon route class to a given path'''
        self.handler.add_route(prefix + route, action)

    def get_root_token(self):
        '''Return a root token for the root user. Used only when requesting it from the internal unix socket'''
        return self.jwt_auth.get_auth_token({'name': 'root', 'method': 'root', 'permissions': ['rw_all']})

    def reload(self, filename, auth_backends):
        '''Reload authentication backends configuration'''
        reloaded_auth = []
        reloaded_conf = []
        try:
            if self.core.reload_conf(filename):
                reloaded_conf.append(filename)
            for auth_backend in auth_backends:
                if self.auth_routes.get(auth_backend):
                    log.debug("Reloading %s auth backend", auth_backend)
                    self.auth_routes[auth_backend].reload()
                    reloaded_auth.append(auth_backend)
                else:
                    log.debug("Authentication backend '%s' not found", auth_backend)
            if len(reloaded_auth) > 0 or len(reloaded_conf) > 0:
                return {'status': falcon.HTTP_200, 'text': f"Reloaded auth '{reloaded_auth}' and conf {reloaded_conf}"}
            else:
                return {'status': falcon.HTTP_404, 'text': 'Error while reloading'}
        except Exception as e:
            log.exception(e)
            return {'status': falcon.HTTP_503}

    def write_and_reload(self, filename, conf, reload_conf, sync=False):
        '''Override the config files and reload. This is mainly used when changing the configuration
        from the web interface.
        '''
        result_dict = {}
        log.debug("Will write to %s config %s and reload %s", filename, conf, reload_conf)
        if filename and conf:
            res = write_config(filename, conf)
            if 'error' in res:
                return {'status': falcon.HTTP_503, 'text': res['error']}
            else:
                result_dict = {'status': falcon.HTTP_200, 'text': f"Reloaded config file {res['file']}"}
        if reload_conf:
            auth_backends = reload_conf.get('auth_backends', [])
            if auth_backends:
                result_dict = self.reload(filename, auth_backends)
            plugins = reload_conf.get('plugins', [])
            if plugins:
                result_dict = self.reload_plugins(plugins)
        if sync and self.cluster:
            self.cluster.write_and_reload(filename, conf, reload_conf)
        return result_dict

    def reload_plugins(self, plugins):
        '''Reload plugins'''
        plugins_error = []
        plugins_success = []
        log.debug("Reloading plugins %s", plugins)
        for plugin_name in plugins:
            plugin = self.core.get_core_plugin(plugin_name)
            if plugin:
                plugin.reload_data()
                plugins_success.append(plugin)
            else:
                plugins_error.append(plugin)
        if plugins_error:
            return {'status': falcon.HTTP_404, 'text': f"The following plugins could not be found: {plugin_error}"}
        else:
            return {'status': falcon.HTTP_200, 'text': "Reloaded plugins: {plugin_success}"}

