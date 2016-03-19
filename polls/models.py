from __future__ import unicode_literals

import datetime

from django.db import models
from django.utils import timezone
from cuser.models import CUser

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    
    def __unicode__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.choice_text

class CUserChoice(models.Model):
    choice= models.ForeignKey(Choice, on_delete=models.CASCADE)
    cuser = models.ForeignKey(CUser, on_delete=models.CASCADE)
    date_vote = models.DateField()
