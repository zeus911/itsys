#!/usr/bin/python
# -*- coding:UTF-8 -*-
# filename:blog.py

import web, re, datetime, time, hashlib, urllib
from urlparse import urlparse

urls = (
    '/index', 'index',
    '/unindex', 'unindex',
    '(.*)', 'reyyc'
)

app_yyc = web.application(urls, globals())
render_yyc = web.template.render('templates/')

class reyyc:
    def GET(self, path):
        #raise web.seeother('/')
        return 'Welcome to here, URI is /blog{0}, path is {0}'.format(path)

class index:
        
    def POST(self):
        i = web.input()
        key = i.key
        #url api获取
        apidomain = urllib.urlopen(i.apidomain)
        domain = apidomain.read()
        apidomain.close()
        #时间处理，当前时间，过期时间
        curdate = datetime.datetime.now()
        curmtime = int(time.mktime(curdate.timetuple()))
        tdate = curdate + datetime.timedelta(days=float(i.days))
        tmtime = int(time.mktime(tdate.timetuple()))
        #获取下载地址
        def createURL(fl):
            if fl == '':
                return
            fls = re.search('[0-9a-f]{32}', fl).group(0)
            md5 = hashlib.md5()
            md5.update(key + fls + str(tmtime))
            k = md5.hexdigest()[8:24]
            return domain + fl + '?k=' + k + '&t=' + str(tmtime)
        #文件地址列表
        urlList = map(createURL, i.filenamelist.strip().split('\r\n'))
        yyc = {
            '生成地址列表': urlList,
            '过期时间': str(tdate),
            '过期毫秒': tmtime,
            '生成时间': str(curdate),
            '生成毫秒': curmtime,
            '域名API': i.apidomain,
            '加密密钥': i.key,
            '歌曲文件列表': i.filenamelist.strip().replace('\r\n', '<br/>'),
            '设置过期时间': i.days,
            '动态域名': domain
        }
        return render_yyc.yyc(yyc)

class unindex:
    def POST(self):
        web.header('Content-Type','text/html; charset=utf-8', unique=True)
        i = web.input()
        parsed = urlparse(i.url)
        #参数解析
        filename = parsed.path
        query = parsed.query
        k = t = ''
        try:
            k = re.search('k=[0-9a-f]{16}', query).group(0)[2:]
        except:
            return 'k值异常'
        try:
            t = re.search('t=\d+', query).group(0)[2:]
            curmtime = int(time.mktime(datetime.datetime.now().timetuple()))
            days = (int(t) - curmtime) / 60 / 60 / 24
            if days > 100:
                return 't值异常，大于100天有效期'
        except:
            return 't值异常'
        tdate = datetime.datetime.fromtimestamp(int(t))
        #加密验证
        filenamestr = re.search('[0-9a-f]{32}', filename).group(0)
        md5 = hashlib.md5()
        md5.update(i.key + filenamestr + t)
        validk = md5.hexdigest()[8:24]
        yyc = {
            '反查地址': i.url + '&nbsp;&nbsp;<a href="' + i.url + '">download</a>',
            '加密密钥': i.key,
            '动态域名': parsed.scheme + '://' + parsed.netloc,
            '过期时间': str(tdate),
            '过期毫秒': t,
            '歌曲文件': filename,
            '加密串k': k,
            '有效加密串k': validk,
            '加密是否有效': (k == validk)
        }
        return render_yyc.yyc(yyc)
