# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-05 16:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flylo', '0028_clientflights_passengers_names'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='seats_occupied',
            field=models.CharField(default='/', max_length=1000, verbose_name='Seats occupied'),
        ),
    ]
