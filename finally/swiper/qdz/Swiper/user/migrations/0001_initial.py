# -*- coding: utf-8 -*-
# Generated by Django 1.11.25 on 2019-11-27 19:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dating_gender', models.CharField(choices=[('male', '男性'), ('female', '女性')], default='Male', max_length=6, verbose_name='匹配性别')),
                ('dating_location', models.CharField(choices=[('北京', '北京'), ('上海', '上海'), ('合肥', '合肥'), ('南京', '南京'), ('深圳', '深圳')], default='上海', max_length=15, verbose_name='目标城市')),
                ('min_distance', models.IntegerField(default=1, verbose_name='最小查找范围')),
                ('max_distance', models.IntegerField(default=10, verbose_name='最大查找范围')),
                ('mim_dating_age', models.IntegerField(default=18, verbose_name='最小交友年龄')),
                ('max_dating_age', models.IntegerField(default=50, verbose_name='最大交友年龄')),
                ('vibration', models.BooleanField(default=True, verbose_name='是否开启震动')),
                ('only_matche', models.BooleanField(default=True, verbose_name='不让来匹配的人看我的相册')),
                ('auto_play', models.BooleanField(default=True, verbose_name='自动播放视频')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phonenum', models.CharField(max_length=15, unique=True)),
                ('nickname', models.CharField(default='匿名用户', max_length=20, null=True)),
                ('sex', models.CharField(choices=[('male', '男性'), ('female', '女性')], default='Male', max_length=6)),
                ('birthday', models.DateField(default='1990-01-01')),
                ('location', models.CharField(choices=[('北京', '北京'), ('上海', '上海'), ('合肥', '合肥'), ('南京', '南京'), ('深圳', '深圳')], default='上海', max_length=56)),
                ('avatar', models.CharField(max_length=256)),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]
