from allauth.account.adapter import DefaultAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_email, user_username, user_field
from allauth.account.models import EmailAddress
from django.conf import settings

from cuser.models import CUser

class CUserSocialAccountAdapter(DefaultSocialAccountAdapter):

    def pre_social_login(self, request, sociallogin):
        print '-------1----->'
        # social account already exists, so this is just a login
        if sociallogin.is_existing:
            return
        print '-------2----->'
        print sociallogin.email_addresses
        # some social logins don't have an email address
        if not sociallogin.email_addresses:
            return
        print '-------3----->'
        email = sociallogin.email_addresses[0]      
        print sociallogin.email_addresses
               
        try:
            user = CUser.objects.get(email__iexact=email.email)
            print '----4-------->'
        except:# EmailAddress.DoesNotExist:
            print '-----5------->'
            return
             
        sociallogin.connect(request, user)    
        
        
        """
               
        for email in sociallogin.email_addresses:
            verified_email = email
            break
        # no verified emails found, nothing more to do
        if not verified_email:
            return
        
        if not not_verified_email:
            return
        
        
        # check if given email address already exists as a verified email on
        # an existing user's account
        try:
            existing_email = EmailAddress.objects.get(email__iexact=email.email, verified=True)
        
        except EmailAddress.DoesNotExist:
            return
        #if it does, connect this new social login to the existing user
        sociallogin.connect(request, existing_email.user)    
        """

"""
class CUserAccountAdapter(DefaultAccountAdapter):
    
     def save_user(self, request, user, form, commit=True):
        user = super(CUserAccountAdapter, self).save_user(request, user, form, commit=False)
        user.is_active = True    
        user.save()
        return user
"""
