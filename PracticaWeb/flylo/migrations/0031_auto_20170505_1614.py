# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-05 16:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flylo', '0030_auto_20170505_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='money',
            field=models.FloatField(verbose_name='User current money'),
        ),
    ]
