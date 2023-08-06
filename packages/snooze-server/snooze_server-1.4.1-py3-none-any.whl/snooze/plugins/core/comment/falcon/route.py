#
# Copyright 2018-2020 Florian Dematraz <florian.dematraz@snoozeweb.net>
# Copyright 2018-2020 Guillaume Ludinard <guillaume.ludi@gmail.com>
# Copyright 2020-2021 Japannext Co., Ltd. <https://www.japannext.co.jp/>
# SPDX-License-Identifier: AFL-3.0
#

'''Comment custom falcon routes.
Mainly used for allowing users to comment as their user only
'''

from logging import getLogger

import bson.json_util
import falcon

from snooze.plugins.core.basic.falcon.route import Route
from snooze.api.falcon import authorize
from snooze.utils import get_modification

log = getLogger('snooze.api')

class CommentRoute(Route):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.notification_plugin = self.core.get_core_plugin('notification')

    @authorize
    def on_post(self, req, resp):
        if self.update_records(req, resp):
            super(CommentRoute, self).on_post(req, resp)

    @authorize
    def on_put(self, req, resp):
        for req_media in req.media:
            req_media['edited'] = True
        if self.update_records(req, resp):
            super(CommentRoute, self).on_put(req, resp)

    @authorize
    def on_delete(self, req, resp, search='[]'):
        if self.delete_records(req, resp, search='[]'):
            super(CommentRoute, self).on_delete(req, resp, search)

    def update_records(self, req, resp):
        update_records = []
        record_comments = {}
        for req_media in req.media:
            if 'record_uid' in req_media:
                notification_from = {'name': req_media.get('name', req.context.get('user', {}).get('user', {}).get('name', '')), 'message': req_media.get('message', '')}
                record_uid = req_media['record_uid']
                record_comments.setdefault(record_uid, []).append(req_media)
                records = self.search('record', record_uid)
                log.debug("Search record %s", record_uid)
                if records['count'] > 0:
                    log.debug("Found record %s", records)
                    media_type = req_media.get('type')
                    comments = self.search('comment', ['=', 'record_uid', record_uid])
                    records['data'][0]['comment_count'] = comments['count'] + len(record_comments[record_uid])
                    if media_type in ['ack', 'esc', 'open', 'close']:
                        log.debug("Changing record %s type to %s", record_uid, media_type)
                        records['data'][0]['state'] = media_type
                        modification_raw = req_media.get('modifications', [])
                        if media_type in ['esc', 'open']:
                            try:
                                for modification in modification_raw:
                                    get_modification(modification, self.core).modify(records['data'][0])
                                if self.notification_plugin:
                                    records['data'][0]['notification_from'] = notification_from
                                    records['data'][0].pop('snoozed', '')
                                    records['data'][0].pop('notifications', '')
                                    self.notification_plugin.process(records['data'][0])
                            except Exception as err:
                                log.exception(err)
                    update_records.append(records['data'][0])
                else:
                    resp.content_type = falcon.MEDIA_TEXT
                    resp.status = falcon.HTTP_503
                    resp.text = f"Record uid {record_uid} was not found"
                    return False
            else:
                resp.content_type = falcon.MEDIA_TEXT
                resp.status = falcon.HTTP_503
                resp.text = 'Comments must contain records uid'
                return False
        if update_records:
            log.debug("Replace records %s", update_records)
            self.core.db.write('record', update_records, duplicate_policy='replace')
        return True

    def delete_records(self, req, resp, search):
        update_records = []
        record_comments = {}
        if 'uid' in req.params:
            cond_or_uid = ['=', 'uid', req.params['uid']]
        else:
            string = req.params.get('s') or search
            try:
                cond_or_uid = bson.json_util.loads(string)
            except Exception:
                cond_or_uid = string
        comments = self.search('comment', cond_or_uid)
        if comments['count'] > 0:
            for comment in comments['data']:
                record_uid = comment['record_uid']
                record_comments.setdefault(record_uid, []).append(comment['uid'])
                records = self.search('record', record_uid)
                log.debug("Search record %s", record_uid)
                if records['count'] > 0:
                    log.debug("Found record %s", records)
                    comments = self.search('comment', ['=', 'record_uid', record_uid],
                        nb_per_page=0, page_number=1, orderby='date', asc=False)
                    records['data'][0]['comment_count'] = comments['count'] - len(record_comments[record_uid])
                    relevant_comments = [
                        com for com in comments['data']
                        if com.get('uid') not in record_comments[record_uid]
                        and com.get('type') in ['ack', 'esc', 'open', 'close']
                    ]
                    log.debug("Relevant comments: %s", relevant_comments)
                    if len(relevant_comments) > 0:
                        new_type = relevant_comments[0]['type']
                        log.debug("Reverting record %s type to %s", record_uid, new_type)
                        records['data'][0]['state'] = new_type
                    else:
                        log.debug("Resetting record %s type", record_uid)
                        records['data'][0]['state'] = ''
                    update_records.append(records['data'][0])
                else:
                    resp.content_type = falcon.MEDIA_TEXT
                    resp.status = falcon.HTTP_503
                    resp.text = f"Record uid {record_uid} was not found"
                    return False
        else:
            resp.content_type = falcon.MEDIA_TEXT
            resp.status = falcon.HTTP_503
            resp.text = 'No record was found matching this comment uid'
            return False
        if update_records:
            log.debug("Update records %s", update_records)
            self.core.db.write('record', update_records)
        return True
