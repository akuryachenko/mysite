from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import CUser

class EmailUserRegistrationForm(forms.ModelForm):
    error_messages = {
        'duplicate_email': _("A user with that email already exists."),
    }
    
    class Meta:
        model = CUser
        fields = ('email',)
    
    
