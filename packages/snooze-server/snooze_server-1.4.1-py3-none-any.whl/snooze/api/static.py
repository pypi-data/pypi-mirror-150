#
# Copyright 2018-2020 Florian Dematraz <florian.dematraz@snoozeweb.net>
# Copyright 2018-2020 Guillaume Ludinard <guillaume.ludi@gmail.com>
# Copyright 2020-2021 Japannext Co., Ltd. <https://www.japannext.co.jp/>
# SPDX-License-Identifier: AFL-3.0
#

'''A static file handler for the Vue web interface'''

import os.path
import mimetypes
from logging import getLogger

import falcon

log = getLogger('snooze')

MAX_AGE = 24 * 3600

class StaticRoute:
    '''Handler route for static files (for the web server)'''
    def __init__(self, root, prefix='', indexes=('index.html',)):
        self.prefix = prefix
        self.indexes = indexes
        self.root = root

    def on_get(self, req, res):
        file = req.path[len(self.prefix):]

        if len(file) > 0 and file.startswith('/'):
            file = file[1:]

        path = os.path.join(self.root, file)
        path = os.path.abspath(path)

        # Prevent top level access
        if not path.startswith(self.root):
            res.stats = falcon.HTTP_403
            return

        # Search for index if directory
        if os.path.isdir(path):
            path = self.search_index(path)
            if not path:
                res.stats = falcon.HTTP_404
                return

        # Type and encoding
        content_type, _encoding = mimetypes.guess_type(path)
        if content_type is not None:
            res.content_type = content_type

        try:
            with open(path, 'rb') as static_file:
                res.cache_control = [f"max-age={MAX_AGE}"]
                res.text = static_file.read()
        except FileNotFoundError as err:
            res.status = falcon.HTTP_404

    def search_index(self, path):
        '''Return the index file when requesting a directory'''
        for index in self.indexes:
            index_file = os.path.join(path, index)
            if os.path.isfile(index_file):
                return index_file
        return None
