import datetime

from django.db import models
from django.db.models import query
from libs.cache import rds
from common import keys


def get(self, *args, **kwargs):
    '''带缓存处理的get方法'''
    model_cls_name = self.model.__name__
    pk = kwargs.get('id') or kwargs.get('pk')
    if pk is not None:
        model_key = keys.MODEL_K % (model_cls_name, pk)
        # 存缓存中获取数据
        model_obj = rds.get(model_key)

        if isinstance(model_obj, self.model):
            return model_obj

    # 缓存中没有数据时， 直接使用原 get 方法从数据库中获取数据
    model_obj = self._get(*args, **kwargs)

    # 将model对象写入缓存
    model_key = keys.MODEL_K % (model_cls_name, model_obj.pk)
    rds.set(model_key, model_obj)

    return model_obj

def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
	'''带缓存处理的 save方法'''

	# 调用原save将数据保存到数据库
	self._save(force_insert, force_update, using, update_fields)

	# 将 model 对象写入缓存
	model_key = keys.MODEL_K %(self.__class__.__name__, self.pk)
	rds.set(model_key, self)


def to_dict(self, *skip_fields):
    '''将 model 对象的字段分装成 dict'''
    attr_dict = {}
    not_safe_type = (datetime.date, datetime.datetime)
    for field in self._meta.fields:
        name = field.attname
        if name not in skip_fields:
            value = getattr(self, name)
            attr_dict[name] = str(value) if isinstance(value, not_safe_type) else value

    return attr_dict


def patch_model():
    '''通过 Monkey Patch 的方式为 Model 增加缓存处理'''
    
    query.QuerySet._get = query.QuerySet.get  # 将原get方法重命名
    query.QuerySet.get = get  # 用带缓存处理的 get 方法覆盖原 get 方法

    models.Model._save = models.Model.save  # 对原save方法进行重命名
    models.Model.save = save  # 用带缓存处理的 save 方法覆盖原 save 方法

    models.Model.to_dict = to_dict