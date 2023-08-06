#
# Copyright 2018-2020 Florian Dematraz <florian.dematraz@snoozeweb.net>
# Copyright 2018-2020 Guillaume Ludinard <guillaume.ludi@gmail.com>
# Copyright 2020-2021 Japannext Co., Ltd. <https://www.japannext.co.jp/>
# SPDX-License-Identifier: AFL-3.0
#

'''Routes for widget'''

from logging import getLogger

import falcon

from snooze.api.falcon import authorize
from snooze.plugins.core.basic.falcon.route import Route
from snooze.api.base import BasicRoute

log = getLogger('snooze.widget')

class WidgetPluginRoute(BasicRoute):
    @authorize
    def on_get(self, req, resp, plugin_name=None):
        log.debug("Listing widgets")
        plugin_name = req.params.get('widget') or plugin_name
        try:
            plugins = []
            loaded_plugins = self.api.core.plugins
            if plugin_name:
                loaded_plugins = [self.api.core.get_core_plugin(plugin_name)]
            for plugin in loaded_plugins:
                plugin_metadata = plugin.get_metadata()
                plugin_widgets = plugin_metadata.get('widgets', {})
                for name, widget in plugin_widgets.items():
                    log.debug("Retrieving widget %s from %s", name, plugin.name)
                    widget['widget_name'] = name
                    plugins.append(widget)
            log.debug("List of widgets: %s", plugins)
            resp.content_type = falcon.MEDIA_JSON
            resp.status = falcon.HTTP_200
            resp.media = {
                'data': plugins,
            }
        except Exception as err:
            log.exception(err)
            resp.status = falcon.HTTP_503

class WidgetRoute(Route):
    @authorize
    def on_post(self, req, resp):
        for req_media in req.media:
            self.inject_meta(req_media)
        super(WidgetRoute, self).on_post(req, resp)

    @authorize
    def on_put(self, req, resp):
        for req_media in req.media:
            self.inject_meta(req_media)
        super(WidgetRoute, self).on_put(req, resp)

    def inject_meta(self, media):
        widget = media.get('widget', [])
        widget_name = widget.get('selected')
        content = widget.get('subcontent')
        plugin = self.api.core.get_core_plugin(widget_name)
        if plugin:
            media['pprint'] = plugin.pprint(content)
        else:
            media['pprint'] = widget_name
        media['icon'] = plugin.get_metadata().get('widgets', {}).get(widget_name, {}).get('icon')
        media['vue_component'] = plugin.get_metadata().get('widgets', {}).get(widget_name, {}).get('vue_component')
