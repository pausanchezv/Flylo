# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-28 06:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flylo', '0025_auto_20170428_0453'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientflights',
            name='is_checked_in',
        ),
        migrations.AddField(
            model_name='clientflights',
            name='category',
            field=models.CharField(default='economic', max_length=20, verbose_name='Flight category'),
        ),
        migrations.AlterField(
            model_name='clientflights',
            name='status',
            field=models.CharField(default='before_checkin', max_length=20, verbose_name='Flight status'),
        ),
    ]
