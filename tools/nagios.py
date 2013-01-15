#!/usr/bin/python
# -*- coding:UTF-8 -*-
# filename:nagios.py

import web, random, string, sqlite3

urls = (
    '/url/index', 'UrlIndex',
    '/url/operate', 'Operate',
    '/url/add', 'UrlAdd',
    '/url/mod', 'UrlMod',
    '/url/pause', 'UrlPause',
    '/url/start', 'UrlStart',
    '/url/del', 'UrlDel',
    '.*', 'UnNagios'
)

app_nagios = web.application(urls, globals())
render_nagios = web.template.render('templates/')
    
# Model

class DBManage:
    
    def fetch(self, sql):
        con = sqlite3.connect("nagios.db")
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        data = cur.fetchall()
        cur.close()
        con.close()
        return data
        
    def execute(self, sql):
        con = sqlite3.connect("nagios.db")
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        con.close()

# URL 数据模型
class UrlModel:
    nid = ''  # 数据编号
    name = ''  # 名称
    url = ''  # 被监控的URL
    contact = ''  # 联系人
    cmd = ''  # 执行命令
    category = ''  # 分类
    status = 0  # 0，开启；1，暂停
        
    def __init__(self, nid='', name='', url='', contact='', cmd='check_url', category='WebUrl', status=0):
        self.nid = nid
        self.name = name
        self.url = url
        self.contact = contact
        self.cmd = cmd
        self.category = category
        self.status = status
        
    def setNid(self, nid):
        self.nid = nid

class Service:
    
    db = DBManage()
    
    def getRandomStr(self, l=5):
        randomList = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        return string.join(random.sample(randomList, l)).replace(' ', '')
    
    def getUrlList(self, operate=''):
        pass
    
    def getUrlByNid(self, nid):
        pass
    
    def addUrl(self, urlModel):
        sql = 'insert inito urlinfo (nid, name, url, contact, cmd, category, status) values ("%s", "%s", "%s"," %s", "%s", "%s", "%s", %d)', (urlModel.nid, urlModel.name, urlModel.url, urlModel.contact, urlModel.cmd, urlModel.category, urlModel.status)
        Service.db.execute(sql)
        
    def modUrl(self, urlModel):
        pass
    
    def delUrl(self, urlModel):
        pass
    
    def pauseUrl(self, urlModel):
        pass
    
    def startUrl(self, urlModel):
        pass

# Controller
class UnNagios:
    def GET(self):
        return 'Please leave immediately! ~\nplease get out here!~'

# 默认操作 Add
class UrlIndex:
    def GET(self):
        operate = 'add'
        urlModelList = []
        service = Service()
        urlModel = UrlModel(nid=service.getRandomStr(5))
        return render_nagios.nagios(operate, urlModel, urlModelList)

# 操作分类
class Operate:
    
    def GET(self):
        i = web.input()
        urlModelList = []
        operate = i.operate
        service = Service()
        if operate == 'add':
            nid = service.getRandomStr(5)
            pass
        elif operate == 'mod':
            nid = i.nid
            pass
        elif operate == 'pause':
            nid = i.nid
            pass
        elif operate == 'start':
            nid = i.nid
            pass
        elif operate == 'del':
            nid = i.nid
            pass
        else:
            pass
        urlModel = UrlModel(nid)
        return render_nagios.nagios(operate, urlModel, urlModelList)
    
# 添加记录
class UrlAdd:
    def POST(self):
        i = web.input()
        urlModelList = []
        operate = i.operate
        service = Service()
        urlModel = UrlModel(nid=i.nid, name=i.name, url=i.url, contact=i.contact, cmd=i.cmd, category=i.category, status=i.status)
#        urlModel = UrlModel()
#        urlModel.nid = i.nid
#        urlModel.setNid(i.nid)
        service.addUrl(urlModel)
        return render_nagios.nagios(operate, urlModel, urlModelList)

# 修改记录    
class UrlMod:
    def POST(self):
        return '正在建设中……'

# 暂停记录    
class UrlPause:
    def POST(self):
        return '正在建设中……'

# 启动记录
class UrlStart:
    def POST(self):
        return '正在建设中……'

# 删除记录
class UrlDel:
    def POST(self):
        return '正在建设中……'


