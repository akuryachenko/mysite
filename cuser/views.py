from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import CreateView
from django.core.signing import Signer
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

from .models import CUser
from .forms import *


class  EmailUserRegistrationView(CreateView):
    model = CUser
    template_name = 'cuser/registration.html'
    form_class =  EmailUserRegistrationForm
    
    email_html_template_name = 'cuser/email.html'
    email_text_template_name = 'cuser/email.txt'
    
    def get_success_url(self):
        return reverse('index')
    
    def form_valid(self, form):
        resp = super(EmailUserRegistrationView, self).form_valid(form)
        user = self.object
        signer = Signer()
        ref_url = ''.join([self.request.build_absolute_uri('/'), 'confirm-email?confirm=', '{}'.format(user.id), ':', signer.sign(user.email)])
        
        txt_body = render_to_string(self.email_text_template_name,
                                    {'reference': ref_url})
                                    
        html_body = render_to_string(self.email_html_template_name,
                                    {'reference': ref_url})
        send_mail(
            recipient_list = [user.email],
            subject = 'Account activation on the website online-polling.com', 
            message=txt_body,
            html_message=html_body,
            from_email = settings.DEFAULT_FROM_EMAIL ,
            fail_silently = True,
        )
        
        return resp
