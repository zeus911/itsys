#!/usr/bin/dev python
# -*- coding:UTF-8 -*-
# filename:index.py

import web
from tools import yyc

urls = (
    '/yyc', yyc.app_yyc, 
    '/', 'index'
)

app = web.application(urls, globals())

class index:
    def GET(self):
        return 'Hello world !'

if __name__ == '__main__':
    app.run()
