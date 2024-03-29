#!/usr/bin/env python

import os
import sys
import random
from datetime import date

import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Swiper.settings")
django.setup()

from user.models import User
from vip.models import VipPermRelation, Vip, Permission

last_names = (
    '赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨'
    '朱秦尤许何吕施张孔曹严华金魏陶姜'
    '戚谢邹喻柏水窦章云苏潘葛奚范彭郎'
    '鲁韦昌马苗凤花方俞任袁柳酆鲍史唐'
    '费廉岑薛雷贺倪汤滕殷罗毕郝邬安常'
    '乐于时傅皮卞齐康伍余元卜顾孟平黄'
)

first_names = {
    'male': [
        '致远', '俊驰', '雨泽', '烨磊', '晟睿',
        '天佑', '文昊', '修洁', '黎昕', '远航',
        '旭尧', '鸿涛', '伟祺', '荣轩', '越泽',
        '浩宇', '瑾瑜', '皓轩', '浦泽', '绍辉',
        '绍祺', '升荣', '圣杰', '晟睿', '思聪'
    ],
    'female': [
        '沛玲', '欣妍', '佳琦', '雅芙', '雨婷',
        '韵寒', '莉姿', '雨婷', '宁馨', '妙菱',
        '心琪', '雯媛', '诗婧', '露洁', '静琪',
        '雅琳', '灵韵', '清菡', '溶月', '素菲',
        '雨嘉', '雅静', '梦洁', '梦璐', '惠茜'
    ]
}

def random_name():
    '''随机产生一个名字'''
    global last_names
    global first_names
    last_name = random.choice(last_names)
    sex = random.choice(list(first_names.keys()))
    first_name = random.choice(first_names[sex])
    return ''.join([last_name, first_name]), sex

def create_robots(n):
    for i in range(n):
        name, sex = random_name()
        year = random.randint(1970, 2000)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        try:
            user = User.objects.create(
                email = '%s' % random.randrange(21000000000,21900000000),
                nickname = name,
                sex = sex,
                birthday = date(year, month, day),
                location = random.choice([item[0] for item in User.LOCATION])
            )
            print('created: %s %s %s' % (user.id, name, sex))
        except django.db.utils.IntegrityError:
            pass

def init_permission():
    '''创建权限模型'''
    permissions = (
      ('vipflag','会员身份标识'),
      ('superlike', '超级喜欢'),
      ('rewind','返回功能'),
      ('anylocation','任意更该定位'),
      ('unlimit_like','无限喜欢次数'),
      ('who_like_me','查看喜欢过我的人'),
    )

    for name, desc in permissions:
      prem, _ = Permission.objects.get_or_create(name=name, desc=desc)
      print('create permission %s' % prem.name)


def init_vip():
    duration = {
      0:1000000,
      1:60,
      2:50,
      3:30,
    }

    for i in range(4):
      vip, _ = Vip.objects.get_or_create(
          name = '%d 级会员' % i,
          level = i,
          price = i * 10.0,
          days = duration[i]
      )
      print('create %s' % vip.name)


def create_vip_perm_relations():
    '''创建vip和permission的关系'''
    # 获取VIp
    vip1 = Vip.objects.get(level=1)
    vip2 = Vip.objects.get(level=2)
    vip3 = Vip.objects.get(level=3)

    # 获取权限
    vipflag = Permission.objects.get(name='vipflag')
    superlike = Permission.objects.get(name='superlike')
    rewind = Permission.objects.get(name='rewind')
    anylocation = Permission.objects.get(name='anylocation')
    unlimit_like = Permission.objects.get(name='unlimit_like')
    who_like_me = Permission.objects.get(name='who_like_me')

    # 给 VIP 1 分配权限
    VipPermRelation.objects.get_or_create(vip_id=vip1.id, perm_id=vipflag.id)
    VipPermRelation.objects.get_or_create(vip_id=vip1.id, perm_id=superlike.id)

    # 给 VIP 2 分配权限
    VipPermRelation.objects.get_or_create(vip_id=vip2.id, perm_id=vipflag.id)
    VipPermRelation.objects.get_or_create(vip_id=vip2.id, perm_id=superlike.id)
    VipPermRelation.objects.get_or_create(vip_id=vip2.id, perm_id=rewind.id)

    # 给 VIP 3 分配权限
    VipPermRelation.objects.get_or_create(vip_id=vip3.id, perm_id=vipflag.id)
    VipPermRelation.objects.get_or_create(vip_id=vip3.id, perm_id=superlike.id)
    VipPermRelation.objects.get_or_create(vip_id=vip3.id, perm_id=rewind.id)
    VipPermRelation.objects.get_or_create(vip_id=vip3.id, perm_id=anylocation.id)
    VipPermRelation.objects.get_or_create(vip_id=vip3.id, perm_id=unlimit_like.id)
    VipPermRelation.objects.get_or_create(vip_id=vip3.id, perm_id=who_like_me.id)

if __name__ == '__main__':
    # create_robots(10000)
    init_permission()
    init_vip()
    create_vip_perm_relations()