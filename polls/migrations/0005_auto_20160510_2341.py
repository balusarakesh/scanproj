# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-10 23:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_auto_20160510_2338'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Choice',
            new_name='Choices',
        ),
    ]
