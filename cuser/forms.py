from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from .models import CUser

class EmailUserRegistrationForm(forms.ModelForm):
    error_messages = {
        'duplicate_email': _("A user with that email already exists."),
    }
    
    class Meta:
        model = CUser
        fields = ('email',)
    
    def save(self, commit=True):
        user = super(EmailUserRegistrationForm, self).save(commit=False)
        user.is_active = False
        if commit:
            user.save()
        return user
    
    
class EmailUserConfirmForm(forms.ModelForm):

    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }

    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html())
    
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput)
    
    daily_reports = forms.BooleanField(
        label=_("Daily reports"),
        widget=forms.CheckboxInput,
        required=False,
        help_text=_("Agree to Receive email daily reports about new polls?"))
    
    class Meta:
        model = CUser
        fields = ('email', 'password1','password2','daily_reports' )
        
        
    def __init__(self, *args, **kwargs):
        super(EmailUserConfirmForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['email'].widget.attrs['readonly'] = True
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        password_validation.validate_password(password1)
        return password2

    def save(self, commit=True):
        user = super(EmailUserConfirmForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.daily_reports = self.cleaned_data['daily_reports']
        user.is_active = True
        if commit:
            user.save()       
        return user


