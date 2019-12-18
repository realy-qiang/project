import datetime

from django.db import models
from vip.models import Vip


# Create your models here.


class User(models.Model):
    '''用户信息'''
    SEX = (
        ('male', '男性'),
        ('female', '女性'),
    )
    LOCATION = (
        ('北京', '北京'),
        ('上海', '上海'),
        ('合肥', '合肥'),
        ('南京', '南京'),
        ('深圳', '深圳'),
    )
    email = models.CharField(max_length=32, unique=True)
    nickname = models.CharField(max_length=20, default='匿名用户', null=True)
    sex = models.CharField(max_length=6, default='Male', choices=SEX)
    birthday = models.DateField(default='1990-01-01')
    location = models.CharField(max_length=56, default='上海', choices=LOCATION)
    avatar = models.CharField(max_length=256)

    vip_id = models.IntegerField(default=1, verbose_name='用户对应的会员 ID')
    vip_end = models.DateTimeField(default='3000-1-1', verbose_name='会员过期时间')

    # profile = models.ForeignKey()

    class Meta:
        db_table = 'user'

    @property
    def profile(self):
        if not hasattr(self, '_profile'):
            self._profile, _ = Profile.objects.get_or_create(id=self.id)
        return self._profile

    @property
    def vip(self):
        if not hasattr(self, '_vip'):
            self._vip = Vip.objects.get(id=self.vip_id)
        return self._vip

    def is_vip_expired(self):
        '''检查会员是否已经过期'''
        return datetime.datetime.now() >= self.vip_end


class Profile(models.Model):

    '''个人资料'''
    dating_gender = models.CharField(
        max_length=6, choices=User.SEX, default='Male', verbose_name='匹配性别')
    dating_location = models.CharField(
        max_length=15, choices=User.LOCATION, default='上海', verbose_name='目标城市')
    min_distance = models.IntegerField(default=1, verbose_name='最小查找范围')
    max_distance = models.IntegerField(default=10, verbose_name='最大查找范围')
    min_dating_age = models.IntegerField(default=18, verbose_name='最小交友年龄')
    max_dating_age = models.IntegerField(default=50, verbose_name='最大交友年龄')
    vibration = models.BooleanField(default=True, verbose_name='是否开启震动')
    only_matche = models.BooleanField(
        default=True, verbose_name='不让来匹配的人看我的相册')
    auto_play = models.BooleanField(default=True, verbose_name='自动播放视频')