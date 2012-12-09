#!/usr/bin/python
# -*- coding:UTF-8 -*-
# filename:hosts.py

import web, re
from _pyio import open

urls = (
    '/index', 'index',
    '/mod', 'mod',
    '(.*)', 'rehosts'
)

app_hosts = web.application(urls, globals())
render_hosts = web.template.render('templates/')

hostsFile = '/etc/hosts'

class rehosts:
    def GET(self, path):
        return 'Welcome to here, URI is /hosts{0}'.format(path)

class index:
    def GET(self):
        web.header('Content-Type', 'text/html; charset=utf-8', unique=True)
        r = open(hostsFile)
        tmpList = r.readlines()
        r.close()
        responseHtml = '<form method="post" action="/hosts/mod">'
        hosts = ''
        for host in tmpList:
            isMatch = bool(re.match(r'^\#?[0-9]+(\.[0-9]+){3}.*$', host, re.VERBOSE));
            if isMatch: 
                hosts += host
        responseHtml += '<textarea name="hosts" cols="60" rows="15">' + hosts + '</textarea><br/>'
        responseHtml += '<input type="submit" value="Update"></form>'
        return responseHtml
    
class mod:
    def POST(self):
        i = web.input()
        w = open(hostsFile, 'w')
        w.writelines(i.hosts)
        w.close()
        # 响应
        web.header('Content-Type', 'text/html; charset=utf-8', unique=True)
        r = open(hostsFile)
        tmpList = r.readlines()
        r.close()
        responseHtml = '<form method="post" action="/hosts/mod">'
        hosts = ''
        for host in tmpList:
            isMatch = bool(re.match(r'^\#?[0-9]+(\.[0-9]+){3}.*$', host, re.VERBOSE));
            if isMatch: 
                hosts += host
        responseHtml += '<textarea name="hosts" cols="60" rows="15">' + hosts + '</textarea><br/>'
        responseHtml += '<input type="submit" value="Update"></form>'
        return responseHtml
