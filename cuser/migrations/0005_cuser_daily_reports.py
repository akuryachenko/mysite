# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-28 04:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuser', '0004_auto_20160326_1727'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuser',
            name='daily_reports',
            field=models.BooleanField(default=False, verbose_name='Do daily reports of new issues?'),
        ),
    ]
