#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__:'Grancis'

#login to URP of SCU use python3

import sys
import io
from urllib import request,parse
from http import cookiejar


class LoginAgent(object):
    def __init__(self):
        self.__cookie=cookiejar.CookieJar() #创建cookie
        self.__cookie_handler=request.HTTPCookieProcessor(self.__cookie) #创建cookie管理器
        self.__http_handler=request.HTTPHandler() #创建http管理器
        self.__https_handler=request.HTTPSHandler() #创建https管理器
        self.__agent=request.build_opener(self.__cookie_handler,self.__http_handler,self.__https_handler)
        self.__login_res=None
        self.__url='http://zhjw.scu.edu.cn/loginAction.do'
        self.__xh=None
        self.__mm=None

    #login method 
    #para: self
    #return __agent with login status
    def login(self):
        self.__xh=input('Input your student ID: ')
        self.__mm=input('Iuput your password: ')
        data=[('zjh',self.__xh),('mm',self.__mm)]
        url_data=parse.urlencode(data)
        #post 请求创建
        req=request.Request(self.__url,data=url_data.encode('utf-8'))
        req.add_header('Origin','http://zhjw.scu.edu.cn')
        req.add_header('Referer','http://zhjw.scu.edu.cn/login.jsp')
        req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36') 
        #用包装好的agent发起request请求 得到一个response返回
        self.__res=self.__agent.open(req)
        return self.__agent
    
    def getRes(self):
        return self.__res


# moduel test
if __name__=='__main__':
    login_agent=LoginAgent()
agent=login_agent.login()
res=login_agent.getRes()

for k,v in res.getheaders():
    print('%s: %s' %(k,v))


