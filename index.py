#!/usr/bin/dev python
# -*- coding:UTF-8 -*-
# filename:index.py

import web
from tools import yyc, hosts

urls = (
    '/yyc', yyc.app_yyc,
    '/hosts', hosts.app_hosts,
    '/', 'index'
)

app = web.application(urls, globals())

class index:
    def GET(self):
        return 'Hello world !'

if __name__ == '__main__':
    app.run()
