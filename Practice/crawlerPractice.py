#!/usr/bim/env python3
# -*- coding: utf-8 -*-
__author__='Grancis'

#crawler pratice using python3 
#target_website: https://www.python.org/events/python-events/
#extrat_content: Time Name & site of the events 
# out: eventInfo 

from html.parser import HTMLParser
from urllib import request
import re

htmlStr=''
req=request.Request('https://www.python.org/events/python-events/')
req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36')
with request.urlopen(req) as f:
    print('Status: ', f.status, f.reason)
    for k, v in f.getheaders():
        print('%s: %s' %(k,v))
    htmlStr=f.read().decode('utf-8')


class Event(object):
    def __init__(self):
        self.__time=None
        self.__name=None
        self.__site=None
        pass
    
    def __str__(self):
        return 'Time: %s \n Name: %s \n Site: %s \n\n\n' %(self.__time, self.__name, self.__site)

    @property
    def time(self):
        return self.__time

    @time.setter
    def time(self,time):
        self.__time=time

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self,name):
        self.__name=name

    @property
    def site(self):
        return self.__site

    @site.setter
    def site(self,site):
        self.__site=site


class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.__flag=False
        self.__info_flag=None
        self.time=[]
        self.name=[]
        self.site=[]

    def handle_starttag(self,tag,attrs):
        if tag=='ul' and re.match(r'list-recent-events',attrs[0][1]):
            self.__flag=True
        elif tag=='a':
            self.__info_flag='name'
        elif tag=='time':
            self.__info_flag='time'
        elif tag=='span' and attrs:
            self.__info_flag='site'

    def handle_endtag(self, tag):
        if tag=='ul':
            self.__flag=False
            
        elif tag=='a':
            self.__info_flag=None
        elif tag=='time':
            self.__info_flag=None
        elif tag=='span':
            self.__info_flag=None

    def handle_data(self,data):
        if self.__flag and self.__info_flag=='time':
            self.time.append(data)
            #print(self.__event.time)
        elif self.__flag and self.__info_flag=='name':
            self.name.append(data)
            #print(self.__event.name)
        elif self.__flag and self.__info_flag=='site':
            m=re.match(r'[a-zA-Z]',data)
            if m:
                self.site.append(data)
                #print(self.__event.site)
                #print('\n')
    
parser = MyHTMLParser()
parser.feed(htmlStr)
eventInfo=[]
for i in range(len(parser.time)):
    event=Event()
    event.time=parser.time[i]
    event.name=parser.name[i]
    event.site=parser.site[i]
    eventInfo.append(event)

for e in eventInfo:
    print(e)
