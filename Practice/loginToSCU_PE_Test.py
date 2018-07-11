#!/usr/bin/env python3
#-*- coding:utf-8 -*-

__author__:'Grancis'

import requests
import re
from html.parser import HTMLParser

_url='https://scusport.com/login'
_headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36','Referer':'https://scusport.com/login','Origin':'https://scusport.com'}
_session=requests.Session()

#用于解析token的parser
class LoginPageParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.__flag=False
        self.token=None
        
    def handle_starttag(self,tag,attrs):
        if tag=='input':
            if attrs[1][1]=='_token':
                self.token=attrs[2][1]

    def handle_endtag(self,tag):
        pass

    def handle_data(self,data):
        pass


#发起post 获得登录过的session
def get_logined_session():
    #获取token 并通过token 构建 post 的data
    _login_page_res=_session.get(_url)
    _token_parser=LoginPageParser()
    _token_parser.feed(_login_page_res.text)
    _token=_token_parser.token
    _scuid=input('Input your student ID: ')
    _password=input('Input your password(教务处密码): ')
    _data={'_token':_token,'scuid':_scuid,'password':_password}
    _login_post_res=_session.post(_url,headers=_headers,data=_data)
    
    if _login_post_res.status_code==200:
        return _session
    else:
        print('login fail, status_code: %s' %_login_page_res.status_code)

#test
if __name__=='__main__':
    res=get_logined_session().get('https://scusport.com/score')
    print(res.text)


