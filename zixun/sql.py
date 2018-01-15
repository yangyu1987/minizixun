#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/18 23:01
# @Author  : Yang
import pymongo
from datetime import datetime

client = pymongo.MongoClient('127.0.0.1',27017)
db = client['zixun']
category = db['cate']
tag = db['tag']
news = db['news']
c_time = datetime.now().strftime('%Y-%m-%d')
# news_data = [
#     {'cate_id':1,'tag_id':1,'title':'测试行业信息1','link':'baidu.com','c_time':c_time,'is_good':1,'source':'36Kr'},
#     {'cate_id':1,'tag_id':2,'title':'测试行业信息2','link':'baidu.com','c_time':c_time,'is_good':1,'source':'搜狗'},
#     {'cate_id':1,'tag_id':2,'title':'测试行业信息3','link':'baidu.com','c_time':c_time,'is_good':1,'source':'虎嗅'},
#     {'cate_id':1,'tag_id':2,'title':'测试2同行发展','link':'baidu.com','c_time':c_time,'is_good':1,'source':'微信'},
#     {'cate_id':1,'tag_id':2,'title':'测试1技术前沿','link':'baidu.com','c_time':c_time,'is_good':1,'source':'未央网'},
#     {'cate_id':1,'tag_id':4,'title':'测试1合作厂商','link':'baidu.com','c_time':c_time,'is_good':1,'source':'凤凰网'},
#     {'cate_id':1,'tag_id':5,'title':'测试1行业会议','link':'baidu.com','c_time':c_time,'is_good':1,'source':'雷锋网'}
# ]
# news_data = [
#     {'cate_id':1,'tag_id':1,'title':'测试商圈信息1','link':'baidu.com','c_time':c_time,'is_good':1,'source':'36Kr'},
#     {'cate_id':1,'tag_id':2,'title':'测试商圈信息1','link':'baidu.com','c_time':c_time,'is_good':1,'source':'雷锋网'},
#     {'cate_id':1,'tag_id':3,'title':'测试商圈信息1','link':'baidu.com','c_time':c_time,'is_good':1,'source':'36Kr'},
#     {'cate_id':1,'tag_id':4,'title':'测试商圈信息1','link':'baidu.com','c_time':c_time,'is_good':1,'source':'36Kr'},
#     {'cate_id':1,'tag_id':5,'title':'测试商圈信息1','link':'baidu.com','c_time':c_time,'is_good':1,'source':'虎嗅网'},
# ]

cate_data = [
    {'cate_id': 1,'cate_name':'金融'},
    {'cate_id': 2,'cate_name':'商圈'},
    {'cate_id': 3,'cate_name':'营销'},
    {'cate_id': 4,'cate_name':'安防/AI'}
]
tag_data4 = [
    { 'tag_id':1,'cate_id':4, 'tag_name':'行业信息'},
    { 'tag_id':2,'cate_id':4, 'tag_name':'同行发展'},
    { 'tag_id':3,'cate_id':4, 'tag_name':'技术前沿'},
    { 'tag_id':4,'cate_id':4, 'tag_name':'合作厂商'},
    { 'tag_id':5,'cate_id':4, 'tag_name':'行业会议'}
]
# tag_data2 = [
#     { 'tag_id':1,'cate_id':2, 'tag_name':'商圈信息'},
#     { 'tag_id':2,'cate_id':2, 'tag_name':'商圈发展'},
#     { 'tag_id':3,'cate_id':2, 'tag_name':'商圈前沿'},
#     { 'tag_id':4,'cate_id':2, 'tag_name':'商圈厂商'},
#     { 'tag_id':5,'cate_id':2, 'tag_name':'商圈会议'}
# ]
for i in cate_data:
    category.insert(i)
for i in tag_data4:
    tag.insert(i)
# for i in tag_data1:
#     tag.insert(i)
# for i in news_data:
#     news.insert(i)
# res = news.find({'cate_id':1},{'tag_id': 1,'title':1})
# res = news.find({'tag_id':{'$in':[1,2]}},{'tag_id': 1,'title':1})
# res = news.find({},{'c_time':1})
# 统一时间格式
# for res1 in res:
#     # print(res1)
#     frags = res1['c_time'].split('-')
#     date = '{}.{}.{}'.format(frags[0],frags[1],frags[2])
#     print(date)
#     news.update_one({'_id':res1['_id']},{'$set':{'c_time':date}})

# from datetime import datetime,timedelta,date
# a = date(2017,12,10)
# print(a)
# d = timedelta(days=1)
# print(d)
# res = news.find({'c_time':{'$in':['2017.12.19']}},{'c_time':1,'title':1})
# # for res1 in res:
# #     print(res1)
#
# # 时间节点生成器
# def get_all_date(date1,date2):
#     start_date = date(int(date1.split('.')[0]),int(date1.split('.')[1]),int(date1.split('.')[2]))
#     end_date = date(int(date2.split('.')[0]), int(date2.split('.')[1]), int(date2.split('.')[2]))
#     days = timedelta(days=1)
#     while start_date <= end_date:
#         yield start_date.strftime('%Y.%m.%d')
#         start_date+=days
#
#
# # for i in get_all_date('2017.6.20','2017.6.20'):
# #     print(i)
#
# # 最近N天时间段
# def get_all_ndate(n):
#     date1 = datetime.now().strftime('%Y.%m.%d')
#     days = timedelta(days=1)
#     end_date = date(int(date1.split('.')[0]),int(date1.split('.')[1]),int(date1.split('.')[2]))
#     start_date = end_date - n*days
#     while start_date <= end_date:
#         yield start_date.strftime('%Y.%m.%d')
#         start_date+=days
#
# for i in get_all_ndate(10):
#     print(i)
#
# def get_data_within(date1,date2,tags):
#     for tag in tags:
#         data_num = []
#         for date in get_all_date(date1,date2):
#             a = list(news.find({'c_time': date, 'tag_id': tag}))
#             data_num.append(len(a))
#         data = {
#             'tag_id':tag,
#             'data':data_num,
#         }
#         yield data
#
# dt = [i for i in get_data_within('2017.12.19','2017.12.19',[1,2,3,4,5])]
#
# pipeline = [
#     {'$match':{'$and':[{'cate_id':1}]}},#大条件
#     {'$group':{'_id':'$tag_id','counts':{'$sum':10}}},#分组统计
#     {'$sort':{'counts':-1}},#倒序
#     {'$limit':3}
# ]
# # for i in news.aggregate(pipeline):
# #     print(i)
#
# pipeline2 = [
#     {'$match':{'$and':[{'c_time':'2017.12.19'},{'cate_id':1}]}},
#     {'$group':{'_id':'$tag_id','counts':{'$sum':1}}},
#     {'$sort':{'counts':-1}},#倒序
#     {'$limit':10}
# ]
# for i in news.aggregate(pipeline2):
#     tag_name =tag.find({'tag_id':i['_id'],'cate_id':1})[0]['tag_name']
#     tag_count = i['counts']
#     data = {
#         'tag_name':tag_name,
#         'tag_count':tag_count
#     }
#     # print(data)