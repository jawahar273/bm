# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-06 11:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20180206_1149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(default='N', max_length=1, verbose_name='Gender'),
        ),
    ]
