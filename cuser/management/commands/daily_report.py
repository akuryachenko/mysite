from __future__ import unicode_literals
from datetime import datetime, timedelta
from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _, activate, deactivate
from django.utils import timezone
from django.contrib.sites.models import Site

from polls.models import Choice, Question, CUserChoice
from cuser.models import CUser


class Command(BaseCommand):
    
    
    def handle(self, *args, **options):
        email_html_template_name = 'cuser/email_report.html'
        email_text_template_name = 'cuser/email_report.txt'
        
        site = Site.objects.get(id=settings.SITE_ID)
        
        now = timezone.now()
        past = timezone.now() - timedelta(days=100)
        from_email = '{}{}'.format(settings.DEFAULT_FROM_EMAIL, site.domain)
        
        new_questions = Question.objects.filter(pub_date__range=(past, now)).order_by('-pub_date')
        users = CUser.objects.filter(daily_reports=True)
        
        for user in users:
            q_u = CUserChoice.objects.filter(cuser=user).values('choice__question')
            question = new_questions.exclude(id__in=q_u).values('question_text',  'pub_date' )
            
            if question:
                txt_body = render_to_string(email_text_template_name, {'report': question, 'site': site.name})
                html_body = render_to_string(email_html_template_name, {'report': question, 'site': site.name})
                
                send_mail(
                    recipient_list = [user.email],
                    subject = 'Daily reports about new polls on the website {}'.format(site.name), 
                    message=txt_body,
                    html_message=html_body,
                    from_email = from_email ,
                    fail_silently = True
                )
                self.stdout.write('Sent mails to {} users'.format(users.count()))
