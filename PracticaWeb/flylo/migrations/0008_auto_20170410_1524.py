# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-10 15:24
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flylo', '0007_auto_20170410_1457'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flight',
            name='airline',
        ),
        migrations.AddField(
            model_name='flight',
            name='airline',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='flylo.Airline'),
            preserve_default=False,
        ),
    ]
