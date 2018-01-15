from django.db import models
import mongoengine
# Create your models here.
from mongoengine import connect

connect('zixun', host='127.0.0.1', port=27017)


class Url(mongoengine.Document):
    crawl_time = mongoengine.StringField(max_length=50)
    comp_id = mongoengine.StringField(max_length=50)
    comp_name = mongoengine.StringField(max_length=50)
    comp_page = mongoengine.StringField(max_length=100)

    meta = {
        'collection':'url'
    }


# for i in Url.objects[:1]:
#     print(i.comp_name)

class Zixun(mongoengine.Document):
    cate_id = mongoengine.IntField(max_length=5)
    tag_id = mongoengine.IntField(max_length=5)
    title = mongoengine.StringField(max_length=50)
    kw= mongoengine.StringField()
    content = mongoengine.StringField()
    link = mongoengine.StringField(max_length=50)
    c_time = mongoengine.StringField(max_length=100)
    is_good = mongoengine.IntField(max_length=5)
    source = mongoengine.StringField(max_length=50)

    meta = {
        'collection':'news'
    }

class Cate(mongoengine.Document):
    cate_id = mongoengine.IntField(max_length=5)
    cate_name = mongoengine.StringField(max_length=50)

    meta = {
        'collection':'cate'
    }


class Tag(mongoengine.Document):
    tag_id = mongoengine.IntField(max_length=5)
    cate_id = mongoengine.IntField(max_length=5)
    tag_name = mongoengine.StringField(max_length=50)

    meta = {
        'collection':'tag'
    }
    # def get_absolute_url(self):
    #     return reverse('tag_id', args=(self.slug,))