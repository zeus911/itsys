#!/usr/bin/python
# -*- coding:UTF-8 -*-
# filename:hosts.py

import web

urls = (
    '/index', 'index',
    '(.*)', 'rehosts'
)

app_hosts = web.application(urls, globals())
render_hosts = web.template.render('templates/')

hostsfile = '/etc/hosts'

class rehosts:
    def GET(self, path):
        return 'Welcome to here, URI is /blog{0}, path is {0}'.format(path)

class index:
    def GET(self):
        r = open(hostsfile)
        hostlist = r.readlines()
        print len(hostlist)
        for i in hostlist:
            print i
        return 'OK'
