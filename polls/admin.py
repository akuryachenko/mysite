from django.contrib import admin

from .models import Choice, Question

import datetime
from django.utils import timezone


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra =2


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date', 'question_img'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'question_img', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']
    
    def was_published_recently(self, obj):
        now = timezone.now()
        return now - datetime.timedelta(days=7) <= obj.pub_date <= now
    
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published last week?'
    
admin.site.register(Question, QuestionAdmin)
