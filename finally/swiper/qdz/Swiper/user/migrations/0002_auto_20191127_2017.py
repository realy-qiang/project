# -*- coding: utf-8 -*-
# Generated by Django 1.11.25 on 2019-11-27 20:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='phonenum',
            new_name='email',
        ),
    ]