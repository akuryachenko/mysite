from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, UpdateView
from django.core.signing import Signer
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils import timezone
from django.contrib.auth import authenticate, login

from polls.models import Choice, Question, CUserChoice
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
       
        ref_url = '{}confirm-email/{}/{}/'.format(self.request.build_absolute_uri('/'), user.id, signer.sign(user.email))
        
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
        #save early voting
        try:
            sch = self.request.session.pop('anonym_vote') #early voting
            ch = Choice.objects.get(pk=sch)
            user_choice = CUserChoice(choice=ch, cuser=user, date_vote = timezone.now())
            user_choice.save()
        except:
            pass
        return resp
        

class  EmailUserConfirmView(UpdateView):
    model = CUser
    template_name = 'cuser/confirm.html'
    form_class =  EmailUserConfirmForm
    
            
    def get_success_url(self):
        return reverse('index')
       
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        signer = Signer()
        s1 = signer.sign(self.object.email)
        s2 = kwargs.get('sign_user', None)
        
        if self.object.is_active == True:
            raise Http404("Account is active yet!")
        
        if s1<>s2:
            raise Http404("Invalid confirm email information")
        
        return super(EmailUserConfirmView, self).dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        ret = super(EmailUserConfirmView, self).form_valid(form)
        user = self.object
        user = authenticate(username=user.email, password=form.cleaned_data["password1"])
        login(self.request, user)
        
        return ret
    
