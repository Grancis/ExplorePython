#!/usr/bin/env python3
#-*-encoding=utf-8-*-

#name 
#team 
#age
#number

import requests
from html.parser import HTMLParser
import json
import re

#爬取所有国家队的url
team_urls=[]
target='https://www.fifa.com/worldcup/teams/'

#建立数据对象Player
class Player(object):
    def __init__(self,team,name,age,number):
        self.team=team
        self.name=name
        self.age=age
        self.number=number

    def __str__(self):
            return 'Team:%s Name:%s Age:%s Number:%s' %(self.team, self.name, self.age, self.number)
    __repr__ = __str__

    def get_team(self):
            return self.team
    def get_name(self):
            return self.name
    def get_age(self):
            return self.age
    def get_number(self):
            return self.number

def player2dict(player):
    return{
        "team":player.team,
        "name":player.name,
        "age":player.age,
        "number":player.number
    }

class TeamUrlParesr(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.__flag=False

    def handle_starttag(self,tag,attrs):
        if tag=='a':
            if len(attrs)>1:
                if len(attrs[0])>1 and len(attrs[1])>1:
                    if attrs[0][1]=='fi-team-card fi-team-card__team':
                        url=target+'team/'+attrs[1][1]
                        team_urls.append(url)
    def handle_endtag(self,tag):
        pass
    def handle_data(self,data):
        pass

#执行TeamParser 获得所有国家队的url 保存在全局变量 team_urls
session=requests.Session()
res=session.get(target)
parser=TeamUrlParesr()
parser.feed(res.text)
#解析一个国家队的所有信息 team name[] num[] list[]
class PlayerParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.__flag=None
        self.team=None
        self.name=[]
        self.num=[]
        self.age=[]
        self.n_team=0
    
    def handle_starttag(self,tag,attrs):
        if tag=='span':
            if len(attrs)>=1:
                if attrs[0][1]=='fi-t__nText ':
                    self.__flag='team'
                    self.n_team+=1
                elif attrs[0][1]=='fi-p__num':
                    self.__flag='num'
                elif re.match(r'fi-p__nShorter',attrs[0][1]):
                    self.__flag='name'
                elif attrs[0][1]=='fi-p__info--ageNum':
                    self.__flag='age'

    def handle_endtag(self,tag):
        if tag=='span':
            self.__flag=None

    def handle_data(self,data):
        if self.__flag=='team' and self.n_team==1:
            self.team=data
        elif self.__flag=='name':
            self.name.append(data)
        elif self.__flag=='num':
            self.num.append(data)
        elif self.__flag=='age':
            self.age.append(data)

#对每个国家队进行逐个解析
#para: url
#return Player[]
def getPlayerList(url):
    players=[]
    res=requests.get(url)
    parser=PlayerParser()
    parser.feed(res.text)
    team=parser.team
    for i in range(len(parser.name)-1):
        player=Player(team,parser.name[i],parser.age[i],parser.num[i])
        players.append(player)
    return players

#循环解析出所有国家的player信息
#para urls
#yeaid players[]
#generator
def getAllPlayerList(urls):
    for url in team_urls:
        yield getPlayerList(url)
    return 'done'


# print(getAllPlayerList(team_urls))

#导出到文件到当前目录的 worldcup_players.json
#bug:json序列化时法语拼写会乱码
# all_players=getAllPlayerList(team_urls)
# with open('./worldcup_players.json','w',encoding='utf-8') as f:
#     for players in all_players:
#         for player in players:
#             f.write(json.dumps(player,default=player2dict))   
#             f.write('\n')


#采用手动拼接json的方法
all_players=getAllPlayerList(team_urls)
def get_json(all_players):
    with open('./worldcup_players.json','w',encoding='utf-8') as f:
        for players in all_players:
            for player in players:
                f.write('{\"team\":\"%s\",\"name\":\"%s\",\"age\":\"%s\",\"number\":\"%s\"}' %(player.team,player.name,player.age,player.number))
                #傻大格式
                # f.write('|%s&%s%%%s@' %(player.team,player.name,player.age))
                f.write('\n')

def get_sql_script():
    with open('./worldcup_players.sql','w',encoding='utf-8') as f:
        for players in all_players:
            for player in players:
                f.write('INSERT INTO player(player_Name,player_Team,player_age,player_Number) VALUES(\"%s\",\"%s\",%d,%d);' %(player.name,player.team,int(player.age),int(player.number)))
                f.write('\n')

get_sql_script()
#test
# print(team_urls[-1])
# players=getPlayerList(team_urls[-1])
# for p in players:
#     print(p)
#     print('\n')


