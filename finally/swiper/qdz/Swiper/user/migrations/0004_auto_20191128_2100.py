# -*- coding: utf-8 -*-
# Generated by Django 1.11.25 on 2019-11-28 21:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20191127_2102'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='mim_dating_age',
            new_name='min_dating_age',
        ),
    ]
