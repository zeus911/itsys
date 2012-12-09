#!/usr/bin/python
# -*- coding:UTF-8 -*-
# filename:nagios.py

import web, random, string

urls = (
    '/url/index', 'UrlIndex',
    '/url/operate', 'Operate',
    '/url/add', 'UrlAdd',
    '/url/mod', 'UrlMod',
    '/url/pause', 'UrlPause',
    '/url/start', 'UrlStart',
    '/url/del', 'UrlDel',
    '(.*)', 'UnNagios'
)

app_nagios = web.application(urls, globals())
render_nagios = web.template.render('templates/')
nagiosList = []

class UnNagios:
    def GET(self, path):
        return 'Welcome to here, URI is /nagios{0}'.format(path)

class Tool:
    def getRandomStr(self, l=5):
        randomList = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
        return string.join(random.sample(randomList, l)).replace(' ', '')

class UrlModel:
    nid = ''
    name = ''
    url = ''
    contact = ''
    cmd = ''
    category = ''
    
    def __init__(self, nid='', name='', url='', contact='', cmd='', category=''):
        self.nid = nid
        self.name = name
        self.url = url
        self.contact = contact
        self.cmd = cmd
        self.category = category
        
class UrlIndex:
    def GET(self):
        operate = 'add'
        tool = Tool()
        nagios = UrlModel(nid=tool.getRandomStr(5))
        return render_nagios.nagios(operate, nagios, nagiosList)

class Operate:
    def GET(self):
        i = web.input()
        operate = i.operate
        nid = i.nid
        if operate == 'add':
            tool = Tool()
            nid=tool.getRandomStr(5)
        elif operate == 'mod':
            pass
        elif operate == 'pause':
            pass
        elif operate == 'start':
            pass
        elif operate == 'del':
            pass
        else:
            pass
        nagios = UrlModel(nid)
        return render_nagios.nagios(operate, nagios, nagiosList)
