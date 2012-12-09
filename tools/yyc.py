#!/usr/bin/python
# -*- coding:UTF-8 -*-
# filename:yyc.py

import web, re, datetime, time, hashlib, urllib, random
from urlparse import urlparse

urls = (
    '/index', 'index',
    '/unindex', 'unindex',
    '/encrypt', 'encrypt',
    '/unencrypt', 'unEncrypt',
    '(.*)', 'reyyc'
)

app_yyc = web.application(urls, globals())
render_yyc = web.template.render('templates/')

class reyyc:
    def GET(self, path):
        return 'Welcome to here, URI is /yyc{0}'.format(path)

class encrypt:
    def POST(self):
        web.header('Content-Type', 'text/html; charset=utf-8', unique=True)
        #参数处理
        i = web.input()
        key = i.key
        domainList = i.domainList
        domain = random.choice(domainList.strip().split('\r\n'))
        uriList = i.uriList
        days = i.days
        #时间处理，当前时间，过期时间
        curdate = datetime.datetime.now()
        tdate = curdate + datetime.timedelta(days=float(days))
        tmtime = int(time.mktime(tdate.timetuple()))
        #获取下载地址
        def createURL(uri):
            if uri == '':
                return
            fls = re.search('[0-9a-f]{32}', uri).group(0)
            md5 = hashlib.md5()
            md5.update(key + fls + str(tmtime))
            k = md5.hexdigest()[8:24]
            url = 'http://' + domain + uri + '?k=' + k + '&t=' + str(tmtime)
            return url + '&nbsp;&nbsp;<a target="_blank" href="' + url + '">download</a><br/>'
        #文件地址列表
        urlList = map(createURL, uriList.strip().split('\r\n'))
        yyc = {
            '生成地址列表': urlList,
            '过期时间': str(tdate),
            '生成时间': str(curdate),
            '加密密钥': i.key,
            '歌曲文件列表': uriList.strip().replace('\r\n', '<br/>'),
            '设置过期时间': i.days,
        }
        return render_yyc.yyc(yyc)
    
class unEncrypt:
    def POST(self):
        web.header('Content-Type', 'text/html; charset=utf-8', unique=True)
        #参数解析
        i = web.input()
        key = i.key
        url = i.url
        parsed = urlparse(i.url)
        uri = parsed.path
        query = parsed.query
        k = t = ''
        try:
            k = re.search('k=[0-9a-f]{16}', query).group(0)[2:]
        except:
            return 'k值异常'
        curmtime = int(time.mktime(datetime.datetime.now().timetuple()))
        try:
            t = re.search('t=\d+', query).group(0)[2:]
            days = (int(t) - curmtime) / 60 / 60 / 24
            if days > 365:
                return 't值异常，大于365天有效期'
        except:
            return 't值异常'
        tdate = datetime.datetime.fromtimestamp(int(t))
        #加密验证
        fls = re.search('[0-9a-f]{32}', uri).group(0)
        md5 = hashlib.md5()
        md5.update(key + fls + t)
        validk = md5.hexdigest()[8:24]
        yyc = {
            '反查地址': url + '&nbsp;&nbsp;<a target="_blank" href="' + url + '">download</a>',
            '加密密钥': key,
            '过期时间': str(tdate),
            '是否有效期内': '<font color="red">' + str(t > curmtime) + "</font>",
            '原始加密串k': k,
            '有效加密串k': validk,
            '加密是否有效': '<font color="red">' + str(k == validk) + "</font>"
        }
        return render_yyc.yyc(yyc)
    
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
        web.header('Content-Type', 'text/html; charset=utf-8', unique=True)
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
