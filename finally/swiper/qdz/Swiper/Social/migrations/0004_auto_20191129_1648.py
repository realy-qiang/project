# -*- coding: utf-8 -*-
# Generated by Django 1.11.25 on 2019-11-29 16:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Social', '0003_auto_20191129_1645'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Fried',
            new_name='Friend',
        ),
    ]