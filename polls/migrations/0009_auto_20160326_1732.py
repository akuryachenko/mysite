# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-26 11:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0008_remove_choice_votes'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cuserchoice',
            unique_together=set([('choice', 'cuser')]),
        ),
    ]
