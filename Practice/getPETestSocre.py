#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__='Grancis'

#爬取川大体侧网站的分数数据并且 将其转换为json数据
import json
import re
import loginToSCU_PE_Test
from html.parser import HTMLParser

_url='https://scusport.com/score'
_session=loginToSCU_PE_Test.get_logined_session()
_res=_session.get(_url)

class ScoreParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.row_1=[]
        self.row_2=[]
        self.__flag=False
        self.__row1_flag=False
        self.__tr_cunt=0

    def handle_starttag(self,tag,attrs):
        if tag=='tr':
            self.__tr_cunt+=1
            if self.__tr_cunt>1:
                self.__flag=True
            
    
    def handle_endtag(self,tag):
        if tag=='tr':
            self.__flag=False
            self.__row1_flag=not self.__row1_flag

    def handle_data(self,data):
        space=re.compile(r'\n')
        if self.__flag and self.__row1_flag and not space.match(data):
            self.row_1.append(data)
        elif self.__flag and not self.__row1_flag and not space.match(data):
            self.row_2.append(data)



def format(row_1,row_2):
    data=[]
    scores=[]
    n=len(row_1)//9
    for i in range(1,n+1):
        d_data={}
        d_scores={}
        d_data['term']=row_1[i*1-1]
        d_data['weight_height']=row_1[i*2-1]
        d_data['lung_cap']=row_1[i*3-1]
        d_data['fifty_run']=row_1[i*4-1]
        d_data['jump']=row_1[i*5-1]
        d_data['sit_reach']=row_1[i*6-1]
        d_data['long_run']=row_1[i*7-1]
        d_data['dif']=row_1[i*8-1]
        d_scores['total']=row_1[i*9-1]
        
        d_scores['term']=row_1[i*1-1]
        d_scores['weight_height']=row_2[i*1-1]
        d_scores['lung_cap']=row_2[i*2-1]
        d_scores['fifty_run']=row_2[i*3-1]
        d_scores['jump']=row_2[i*4-1]
        d_scores['sit_reach']=row_2[i*5-1]
        d_scores['long_run']=row_2[i*6-1]
        d_scores['dif']=row_2[i*7-1]

        data.append(d_data)
        scores.append(d_scores)
    return (data,scores)


#返回 测试数据 测试成绩 (data,scores)
def get_data_scores():
    score_parser=ScoreParser()
    score_parser.feed(_res.text)
    return format(score_parser.row_1,score_parser.row_2)

#test
if __name__=='__main__':
    (data,scores)=get_data_scores()
    print(data)
    print('\n')
    print(scores)