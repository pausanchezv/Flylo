# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-10 14:03
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flylo', '0004_auto_20170410_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aircraft',
            name='airline',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flylo.Airline'),
        ),
    ]
