# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-10 19:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='scanmodel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.TextField(max_length=200)),
                ('resultsurl', models.TextField(max_length=2000)),
                ('status', models.TextField(max_length=11)),
            ],
        ),
    ]
