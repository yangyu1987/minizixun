from django.shortcuts import render
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.http import HttpRequest
from zixun.models import Url
from zixun.models import *
from mongoengine.queryset.visitor import Q
from datetime import datetime,timedelta,date
import json
from django.http import HttpResponse
# Create your views here.


def index(request):
    # 首页
    com_info = Url.objects
    p = Paginator(com_info, 10)# 每个页面展示10个
    page = request.GET.get('page',1)
    contacts = {
        'comps': p.page(page)
    }
    return render(request,'zixun/index.html',contacts)


def add_num(requset):
    return HttpResponse('ajax 实例')

def ajax(request):
    return render(request,'zixun/ajax.html')

def maowan(request):
    return render(request,'zixun/maowan.html')

def zixun(request):
    # 首页
    kw = request.GET.get('kw')
    com_info = Zixun.objects(kw=kw)
    all_num = len(com_info)
    p = Paginator(com_info, 10)  # 每个页面展示10个
    page = request.GET.get('page', 1)
    contacts = {
        'zixun': p.page(page)
    }

    return render(request,'zixun/zixun.html',contacts)


def zxitem(request):
    # 首页
    kw = request.GET.get('kw')
    info = Zixun.objects(kw=kw)
    all_num = len(info)
    p = Paginator(info, 20)  # 每个页面展示10个
    page = request.GET.get('page', 1)
    contacts = {
        'zixun': p.page(page),
        'kw':kw
    }

    return render(request,'zixun/zixunitem.html',contacts)

def jr(request,cate_id):
    # 首页
    # kw = request.GET.get('kw')
    # info = Zixun.objects(kw=kw)
    # all_num = len(info)
    # p = Paginator(info, 20)  # 每个页面展示10个
    # page = request.GET.get('page', 1)
    # contacts = {
    #     'zixun': p.page(page),
    #     'kw':kw
    # }
    cate =Cate.objects(cate_id = cate_id)
    tag = Tag.objects(cate_id = cate_id)
    # cate info
    all_cate = Cate.objects()
    cate_info = []
    for i in all_cate:
        all_cate_dict = {}
        all_cate_dict['cate_id'] = i['cate_id']
        all_cate_dict['cate_name'] = i['cate_name']
        cate_all_tag = Tag.objects(cate_id=i.cate_id)
        cate_tag_list = []
        for t in cate_all_tag:
            cate_tag_info = {}
            cate_tag_info['tag_id'] = t.tag_id
            cate_tag_info['tag_name'] = t.tag_name
            cate_tag_list.append(cate_tag_info)

        all_cate_dict['cate_tag_info'] = cate_tag_list
        cate_info.append(all_cate_dict)
    # end cate info
    n_time = datetime.now().strftime('%Y-%m-%d')
    # 文今日章统计
    pipe_today_article = [
        {'$match': {'$and': [{'cate_id': int(cate_id)},{'c_time':n_time}]}},  # 大条件
        {'$group': {'_id': '$cate_id', 'counts': {'$sum': 1}}},  # 分组统计
        {'$sort': {'counts': -1}},
        {'$limit': 10}
    ]
    today_article = []
    for i in Zixun._get_collection().aggregate(pipe_today_article):
        today_article.append(i['counts'])

    # 历史文章统计
    pipe_all_article = [
        {'$match': {'$and': [{'cate_id': int(cate_id)}]}},  # 大条件
        {'$group': {'_id': '$cate_id', 'counts': {'$sum': 1}}},  # 分组统计
        {'$sort': {'counts': -1}},
        {'$limit': 10}
    ]
    all_article =[]
    for i in Zixun._get_collection().aggregate(pipe_all_article):
        all_article.append(i['counts'])
    # 来源统计
    pipe_source = [
        {'$match': {'$and': [{'cate_id': int(cate_id)}]}},  # 大条件
        {'$group': {'_id': '$source', 'counts': {'$sum': 1}}},  # 分组统计
        {'$sort': {'counts': -1}},
        {'$limit': 10}
    ]
    source_data = []
    source_leg = []
    for i in Zixun._get_collection().aggregate(pipe_source):
        source_data.append({'value':i['counts'],'name':i['_id']})
        source_leg.append(i['_id'])

    # 板块发布量统计
    tg_name_leg = []
    tg_seris_data = []
    time_line = []
    for date in get_all_ndate(6):
        time_line.append(date)
    for tg in tag:
        date_artical_num_data = []
        for date in get_all_ndate(6):
            pipe_date_artical_num = [
                {'$match': {'$and': [{'cate_id': int(cate_id)},{'c_time':date},{'tag_id':tg['tag_id']}]}},  # 大条件
                {'$group': {'_id': '$tag_id', 'counts': {'$sum': 1}}},  # 分组统计
                # {'$sort': {'counts': -1}},
                {'$limit': 7}
            ]
            date_artical_num_data.append(0)
            for i in Zixun._get_collection().aggregate(pipe_date_artical_num):
                date_artical_num_data.append(i['counts'])

        tg_name_leg.append(tg['tag_name'])
        art_item = {
            'name':tg['tag_name'],
            'type': 'line',
            'stack': '总量',
            'areaStyle': {'normal': {}},
            'data': date_artical_num_data
        }
        tg_seris_data.append(art_item)

    # 热词统计
    pipe_today_kw = [
        # {'$match': {'$and': [{'cate_id': int(cate_id)}, {'c_time': n_time}]}},  # 大条件
        {'$match': {'$and': [{'cate_id': int(cate_id)}]}},  # 大条件
        {'$group': {'_id': '$kw', 'counts': {'$sum': 1}}},  # 分组统计
        {'$sort': {'counts': -1}},
        {'$limit': 100}
    ]
    today_kw = []
    for i in Zixun._get_collection().aggregate(pipe_today_kw):
        today_kw.extend(i['_id'])

    k_s = {}# 词频字典
    for i in today_kw:
        if today_kw.count(i) > 1:
            k_s[i] = today_kw.count(i)

    data_kw = []
    data_kw_num = []
    for i in sorted(k_s.items(), key=lambda item: item[1])[-15:]:
        data_kw.append(i[0])
        data_kw_num.append(i[1])

    if today_article:
        today_article = today_article[0]
    else:
        today_article=''
    if all_article:
        all_article = all_article[0]
    else:
        all_article = ''
    contacts = {
        'tags': tag,
        'cate_id':cate_id,
        'cate_name': cate,
        'today_article':today_article,
        'all_article':all_article,
        'source_leg':source_leg,
        'source_data':source_data,
        'data_kw':data_kw,
        'data_kw_num':data_kw_num,
        'tg_name_leg':tg_name_leg,
        'tg_seris_data':tg_seris_data,
        'time_line':time_line,
        'all_cate': cate_info,
    }
    return render(request,'zixun/zixun.html',context=contacts)

def jr_detial(request,cate_id,tag_id):
    # 首页
    # kw = request.GET.get('kw')
    # info = Zixun.objects(kw=kw)
    # all_num = len(info)
    # p = Paginator(info, 20)  # 每个页面展示10个
    # page = request.GET.get('page', 1)
    # contacts = {
    #     'zixun': p.page(page),
    #     'kw':kw
    # }
    # kw = request.GET.get('kw')
    cate = Cate.objects(cate_id=cate_id)
    tag = Tag.objects(cate_id=cate_id)
    # cate info
    all_cate = Cate.objects()
    cate_info = []
    for i in all_cate:
        all_cate_dict = {}
        all_cate_dict['cate_id'] = i['cate_id']
        all_cate_dict['cate_name'] = i['cate_name']
        cate_all_tag = Tag.objects(cate_id=i.cate_id)
        cate_tag_list = []
        for t in cate_all_tag:
            cate_tag_info = {}
            cate_tag_info['tag_id'] = t.tag_id
            cate_tag_info['tag_name'] = t.tag_name
            cate_tag_list.append(cate_tag_info)

        all_cate_dict['cate_tag_info'] = cate_tag_list
        cate_info.append(all_cate_dict)
    # end cate info
    n_time = datetime.now().strftime('%Y-%m-%d')
    # 文今日章统计
    pipe_today_article = [
        {'$match': {'$and': [{'cate_id': int(cate_id)}, {'c_time': n_time}]}},  # 大条件
        {'$group': {'_id': '$cate_id', 'counts': {'$sum': 1}}},  # 分组统计
        {'$sort': {'counts': -1}},
        {'$limit': 10}
    ]
    today_article = []
    for i in Zixun._get_collection().aggregate(pipe_today_article):
        today_article.append(i['counts'])

    # 历史文章统计
    pipe_all_article = [
        {'$match': {'$and': [{'cate_id': int(cate_id)}]}},  # 大条件
        {'$group': {'_id': '$cate_id', 'counts': {'$sum': 1}}},  # 分组统计
        {'$sort': {'counts': -1}},
        {'$limit': 10}
    ]
    all_article = []
    for i in Zixun._get_collection().aggregate(pipe_all_article):
        all_article.append(i['counts'])

    info = Zixun.objects(Q(tag_id = tag_id)&Q(cate_id = cate_id))
    info_pipe = [
        {'$match':{'$and':[{'cate_id': int(cate_id)}, {'tag_id': int(tag_id)}]}},
        # {'$group':{'_id':'$c_time','counts':{'$sum':1}}},
        {'$sort': {'c_time': -1}},
        {'$limit': 100}
    ]
    import random
    info_acrticle = []
    for i in Zixun._get_collection().aggregate(info_pipe):
        info_acrticle.append(i)
    random_info_acrticle = random.sample(info_acrticle,len(info_acrticle)-1)
    # 热词统计
    pipe_today_kw = [
        # {'$match': {'$and': [{'cate_id': int(cate_id)},{'tag_id': int(tag_id)}, {'c_time': n_time}]}},  # 大条件
        {'$match': {'$and': [{'cate_id': int(cate_id)}, {'tag_id': int(tag_id)}]}},  # 大条件
        {'$group': {'_id': '$kw', 'counts': {'$sum': 1}}},  # 分组统计
        {'$sort': {'counts': -1}},
        {'$limit': 20}
    ]
    today_kw = []
    for i in Zixun._get_collection().aggregate(pipe_today_kw):
        today_kw.extend(i['_id'])

    k_s = {}  # 词频字典
    for i in today_kw:
        if today_kw.count(i) > 1:
            k_s[i] = today_kw.count(i)

    data_kw = []
    data_kw_dic = []
    for i in sorted(k_s.items(), key=lambda item: item[1])[-10:]:
        data_kw.append(i[0])
        data_kw_dic.append({'value': i[1], 'name': i[0]})

    if today_article:
        today_article = today_article[0]
    else:
        today_article=''
    if all_article:
        all_article = all_article[0]
    else:
        all_article = ''
    contacts = {
        'tags': tag,
        # 'zixun':info_acrticle,
        'zixun':random_info_acrticle,
        # 'zixun1':info_acrticle,
        'cate_name': cate,
        'cate_id':cate_id,
        'today_article': today_article,
        'all_article': all_article,
        'data_kw':data_kw,
        'data_kw_dic':data_kw_dic,
        'now_tag_id':int(tag_id),
        'all_cate':cate_info,
    }
    return render(request,'zixun/zixunitem.html',context=contacts)

########移动端########
def mnews(request):
    return render(request,'zixun/mobile/news.html')

########工具函数########
def get_all_ndate(n):
    date1 = datetime.now().strftime('%Y-%m-%d')
    days = timedelta(days=1)
    end_date = date(int(date1.split('-')[0]),int(date1.split('-')[1]),int(date1.split('-')[2]))
    start_date = end_date - n*days
    while start_date <= end_date:
        yield start_date.strftime('%Y-%m-%d')
        start_date+=days