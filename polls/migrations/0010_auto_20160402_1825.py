# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-02 12:25
from __future__ import unicode_literals

from django.db import migrations, models
import polls.models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_auto_20160326_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_img',
            field=models.ImageField(blank=True, upload_to=polls.models.normalization_file_name),
        ),
    ]