# -*- coding: utf-8 -*-
# Generated by Django 1.11.25 on 2019-11-27 21:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20191127_2017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(max_length=32, unique=True),
        ),
    ]
