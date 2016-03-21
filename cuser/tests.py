from django.test import TestCase, Client
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.core.signing import Signer
from django import forms 
from django.core.urlresolvers import reverse
import datetime


from polls.models import *
from .models  import *



def create_superuser(email, password):
    return CUser.objects.create_superuser(email=email, password=password)

def create_user(email):
    return CUser.objects.create_user(email=email)

class CUserMethodTests(TestCase):
    
    def test_create_super_user(self):
        user = create_superuser("ainf23@mail.ru", "111") 
        
        self.assertEqual(user.email, "ainf23@mail.ru")
        self.assertEqual(check_password("111", user.password), True )
        self.assertNotEqual(check_password("112", user.password), True )
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_admin, True)
        self.assertEqual(user.is_staff, True)
        self.assertEqual(user.get_full_name(), "ainf23@mail.ru")
        self.assertEqual(user.get_short_name(), "ainf23@mail.ru")
        self.assertEqual(user.__unicode__(), "ainf23@mail.ru")
        self.assertEqual(user.has_perm(None), True)
        self.assertEqual(user.has_module_perms(None), True)
        self.assertEqual(user.username, "ainf23@mail.ru")        
        CUser.objects.all().delete
                
    
    def test_create_super_user_none_email(self):
        with self.assertRaisesRegexp(ValueError, 'The given email must be set'): 
            create_superuser("", "111")
            
    def test_create_user(self):
        user = create_user("ainf23@rambler.ru") 
        
        self.assertEqual(user.email, "ainf23@rambler.ru")
        #self.assertEqual(check_password(None, user.password), True )
        self.assertEqual(user.is_active, False)
        self.assertEqual(user.is_admin, False)
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.get_full_name(), "ainf23@rambler.ru")
        self.assertEqual(user.get_short_name(), "ainf23@rambler.ru")
        self.assertEqual(user.__unicode__(), "ainf23@rambler.ru")
        self.assertEqual(user.has_perm(None), True)
        self.assertEqual(user.has_module_perms(None), True)
        self.assertEqual(user.username, "ainf23@rambler.ru")        
        CUser.objects.all().delete
        
    def test_create_user_user_none_email(self):
        with self.assertRaisesRegexp(ValueError, 'The given email must be set'): 
            create_user("",)
    

class CUserViewFormTests(TestCase):
    
    def test_login_superuser(self):
        create_superuser("ainf23@mail.ru", "111") 
        log = self.client.login(username='ainf23@mail.ru', password='111')
        self.assertEqual(log, True)
        
        response = self.client.post('/registration/', {'email':'ainf23@mail.ru'})
        self.assertContains(response, "User with this Email address already exists")
        CUser.objects.all().delete

    def test_registration_and_confirm_user(self):
        response = self.client.post('/registration/', {'email':'ainf23@mail.ru'})
              
        self.assertIn('reference',response.context)
        
        ref = response.context['reference']
                
        signer = Signer()        
        sign = signer.sign("ainf23@mail.ru")
        
        self.assertRegexpMatches(ref, sign)
                
        response = self.client.post(ref, {'email':'ainf23@mail.ru', 'password1':'222', 'password2':'222'})
           
        log = self.client.login(username='ainf23@mail.ru', password='222')
        self.assertEqual(log, True)
        CUser.objects.all().delete
    
    def test_registration_user_incorrect_email(self):
        response = self.client.post('/registration/', {'email':'ainf23mail.ru'})
        self.assertContains(response, "Enter a valid email address")
        self.assertNotIn('reference',response.context)
        CUser.objects.all().delete    
    
    def test_registration_and_confirm_user_password_missmatch(self):
        response = self.client.post('/registration/', {'email':'ainf23@mail.ru'})
        ref = response.context['reference']
             
        response = self.client.post(ref, {'email':'ainf23@mail.ru', 'password1':'222', 'password2':'333'})
        self.assertContains(response, "The two password fields didn&#39;t match.")
        
        CUser.objects.all().delete
        
    def test_registration_and_confirm_user_bad_refference (self):
        response = self.client.post('/registration/', {'email':'ainf23@mail.ru'})
        ref = response.context['reference']
        ref = ref.replace("ainf23@mail.ru","ainf24@mail.ru")
        response = self.client.post(ref, {'email':'ainf24@mail.ru', 'password1':'222', 'password2':'222'})
        self.assertEqual(response.status_code, 404)        
        
        log = self.client.login(username='ainf24@mail.ru', password='222')
        self.assertEqual(log, False)
        CUser.objects.all().delete
        


