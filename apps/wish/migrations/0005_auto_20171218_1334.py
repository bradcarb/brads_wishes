# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-18 20:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wish', '0004_auto_20171218_1325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_hired',
            field=models.DateField(),
        ),
    ]
