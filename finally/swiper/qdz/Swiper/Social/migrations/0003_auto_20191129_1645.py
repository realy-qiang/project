# -*- coding: utf-8 -*-
# Generated by Django 1.11.25 on 2019-11-29 16:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Social', '0002_auto_20191129_1632'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='fried',
            unique_together=set([('uid1', 'uid2')]),
        ),
    ]
