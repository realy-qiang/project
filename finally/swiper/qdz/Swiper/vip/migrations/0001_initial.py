# -*- coding: utf-8 -*-
# Generated by Django 1.11.25 on 2019-12-03 17:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='权限描述')),
                ('desc', models.TextField(verbose_name='权限描述')),
            ],
        ),
        migrations.CreateModel(
            name='Vip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, unique=True, verbose_name='会员名称')),
                ('level', models.IntegerField(default=0, verbose_name='会员等级')),
                ('price', models.FloatField(default=0.0, verbose_name='会员价格')),
                ('days', models.IntegerField(default=0, verbose_name='天数')),
            ],
        ),
        migrations.CreateModel(
            name='VipPermRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vip_id', models.IntegerField(verbose_name='会员ID')),
                ('perm_id', models.IntegerField(verbose_name='权限ID')),
            ],
        ),
    ]
