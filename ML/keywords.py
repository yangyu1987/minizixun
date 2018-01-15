#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/19 21:01
# @Author  : Yang
import pymongo
from datetime import datetime

client = pymongo.MongoClient('127.0.0.1',27017)
db = client['zixun']
category = db['cate']
tag = db['tag']
news = db['news']
c_time = datetime.now().strftime('%Y-%m-%d')