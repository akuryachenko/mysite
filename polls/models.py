from __future__ import unicode_literals

import os
import datetime
from django.conf import settings
from django.db import models
from django.utils import timezone
from cuser.models import CUser
"""
def normalization_file_name(instance, filename):
    new_name = 1
    for root, dirs, files in os.walk(settings.MEDIA_ROOT):
        for i in files:
            f = os.path.splitext(i)[0]
            if f.isdigit():
                if int(f) >= new_name:
                    new_name =  int(f)+1                     
        break
    return "{}{}".format(new_name, os.path.splitext(filename)[1])
"""
def normalization_file_name(instance, filename):
    return "img{}".format(os.path.splitext(filename)[1])

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    question_img = models.ImageField(blank=True, upload_to=normalization_file_name)
    
    def __unicode__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=7) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    #votes = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.choice_text

class CUserChoice(models.Model):
    choice= models.ForeignKey(Choice, on_delete=models.CASCADE)
    cuser = models.ForeignKey(CUser, on_delete=models.CASCADE)
    date_vote = models.DateField()
    
    class Meta:
        unique_together = ("choice", "cuser")
