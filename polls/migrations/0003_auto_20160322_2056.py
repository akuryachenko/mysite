# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-22 14:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_cuserchoice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuserchoice',
            name='cuser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cuser.CUser'),
        ),
    ]
