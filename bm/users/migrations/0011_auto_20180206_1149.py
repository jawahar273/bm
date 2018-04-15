# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-06 11:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_userprofilesettings_currency_details'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofilesettings',
            name='email',
        ),
        migrations.RemoveField(
            model_name='userprofilesettings',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='userprofilesettings',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='userprofilesettings',
            name='last_name',
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(default='M', max_length=1, verbose_name='Gender'),
        ),
        migrations.AlterField(
            model_name='userprofilesettings',
            name='currency_details',
            field=models.TextField(default='', max_length=100, verbose_name='Currency Details'),
        ),
    ]
