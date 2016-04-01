from django.test import TestCase, Client
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.core.signing import Signer
from django.core.exceptions import ValidationError
from django import forms 
from django.core.urlresolvers import reverse
import datetime
from django.template.loader import render_to_string
from django.contrib.sessions.models import Session
from django.template.loader import render_to_string

from polls.models import *
from .models  import *

def ClearModels():
    CUser.objects.all().delete    
    Question.objects.all().delete 
    Choice.objects.all().delete 
    CUserChoice.objects.all().delete 
        

def create_superuser(email, password):
    return CUser.objects.create_superuser(email=email, password=password)

def create_user(email):
    return CUser.objects.create_user(email=email)

class CUserModelTests(TestCase):
    
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
        
        ClearModels()
                
    
    def test_create_super_user_none_email(self):
        with self.assertRaisesRegexp(ValueError, 'The given email must be set'): 
            create_superuser("", "111")
            
    def test_create_user(self):
        user = create_user("ainf23@rambler.ru") 
        CUser.objects.all().delete    
        Question.objects.all().delete 
        Choice.objects.all().delete 
        CUserChoice.objects.all().delete 
        
        self.assertEqual(user.email, "ainf23@rambler.ru")
        self.assertEqual(user.is_active, False)
        self.assertEqual(user.is_admin, False)
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.get_full_name(), "ainf23@rambler.ru")
        self.assertEqual(user.get_short_name(), "ainf23@rambler.ru")
        self.assertEqual(user.__unicode__(), "ainf23@rambler.ru")
        self.assertEqual(user.has_perm(None), True)
        self.assertEqual(user.has_module_perms(None), True)
        self.assertEqual(user.username, "ainf23@rambler.ru")        
        
        ClearModels()
        
    def test_create_user_user_none_email(self):
        with self.assertRaisesRegexp(ValueError, 'The given email must be set'): 
            create_user("",)
    
    def test_login_superuser(self):
        create_superuser("ainf23@mail.ru", "111") 
        log = self.client.login(username='ainf23@mail.ru', password='111')
        self.assertEqual(log, True)
        response = self.client.post('/registration/', {'email':'ainf23@mail.ru'})
        self.assertContains(response, "User with this Email address already exists")
        ClearModels()
    
    def test_registration_and_confirm_user(self):
        response = self.client.post('/registration/', {'email':'ainf23@mail.ru'})
              
        self.assertIn('reference',response.context)
        
        ref = response.context['reference']
                
        signer = Signer()        
        sign = signer.signature("ainf23@mail.ru")
        
        self.assertRegexpMatches(ref, sign)
                
        response = self.client.post(ref, {'email':'ainf23@mail.ru', 'password1':'Coxb2014', 'password2':'Coxb2014'})
           
        log = self.client.login(username='ainf23@mail.ru', password='Coxb2014')
        self.assertTrue(log)
        
        ClearModels()
        
    def test_registration_and_confirm_active_user(self):
        response = self.client.post('/registration/', {'email':'ainf23@mail.ru'})
        ref = response.context['reference']
        response = self.client.post(ref, {'email':'ainf23@mail.ru', 'password1':'Coxb2014', 'password2':'Coxb2014'})        
        response = self.client.post(ref, {'email':'ainf23@mail.ru', 'password1':'222', 'password2':'222'})
        #self.assertContains(response, "Account is active yet!")
        self.assertEqual(response.status_code, 404)
        ClearModels()
   
    def test_registration_user_incorrect_email(self):
        response = self.client.post('/registration/', {'email':'ainf23mail.ru'})
        self.assertContains(response, "Enter a valid email address")
        self.assertNotIn('reference',response.context)
        ClearModels()
    
    def test_registration_and_confirm_user_password_missmatch(self):
        response = self.client.post('/registration/', {'email':'ainf23@mail.ru'})
        ref = response.context['reference']
        response = self.client.post(ref, {'email':'ainf23@mail.ru', 'password1':'222', 'password2':'333'})
        self.assertContains(response, "The two password fields didn&#39;t match.")
        ClearModels()
        
    def test_registration_and_confirm_user_password_weak(self):
        response = self.client.post('/registration/', {'email':'ainf23@mail.ru'})
        ref = response.context['reference']
        
        response = self.client.post(ref, {'email':'ainf23@mail.ru', 'password1':'222', 'password2':'222'})
        self.assertContains(response, "This password is too short")
        self.assertContains(response, "It must contain at least 8 characters.")
        self.assertContains(response, "This password is entirely numeric.")
        
        ClearModels()
        
    def test_registration_and_confirm_user_bad_refference (self):
        response = self.client.post('/registration/', {'email':'ainf23@mail.ru'})
        ref = response.context['reference']
        ref2 = ref[:-2] + '/'
        response = self.client.post(ref2, {'email':'ainf23@mail.ru', 'password1':'Cjxb2014', 'password2':'Cjxb2014'})
        self.assertEqual(response.status_code, 404)
        ref2 = ref.replace('/1/','/2/')
        esponse = self.client.post(ref2, {'email':'ainf23@mail.ru', 'password1':'Cjxb2014', 'password2':'Cjxb2014'})
        self.assertEqual(response.status_code, 404)
        
        log = self.client.login(username='ainf23@mail.ru', password='Cjxb2014')
        self.assertEqual(log, False)        
        ClearModels()
        
        #rendered = render_to_string("cuser/tests.html",) 


def create_question_choice(question_text, choice_text):   
    question  = Question.objects.create(question_text=question_text, pub_date=timezone.now())
    choice = Choice.objects.create(question = question, choice_text = choice_text)
    return (question, choice)


    
class CUserPollsTests(TestCase):
    def user_add(self):
        response = self.client.post('/registration/', {'email':'ainf23@mail.ru'})
        self.assertIn('reference',response.context)
        ref = response.context['reference']        
        response = self.client.post(ref, {'email':'ainf23@mail.ru', 'password1':'Coxb2014', 'password2':'Coxb2014'})     
        self.client.login(username="ainf23@rambler.ru", password="Cjxb2014")
            
    def user_login(self):
        self.client.login(username="ainf23@rambler.ru", password="Cjxb2014")
        
        
    def user_log_out(self):
        self.client.logout()
        
    
    def test_vote_anonymous_user(self):

        ret = create_question_choice("Who are you?", "Man")
        
        response = self.client.get(reverse('index'))         
        self.assertContains(response, "Man")
        
        #unavailability userresults page for anonymous_user 
        response = self.client.post('userresults')
        self.assertEqual(response.status_code, 404) 
        
        response = self.client.get(reverse('detail',
                                   args=(ret[0].id,)))
        self.assertContains(response, ret[0].question_text,
                            status_code=200)
             
        #early vote
        response = self.client.post("/{}/".format(ret[0].id), {'ch':ret[1].id})
        #self.assertContains(response, "In order to vote you must register")
        
        #session = self.client.session
        #session['anonym_vote'] = ret[1].id
        #session.save()
        
        response= self.client.post('/registration/', {'email':'ainf23@mail.ru'})
        ref = response.context['reference']
        self.assertTrue(CUserChoice.objects.filter(choice = ret[1]).exists())            
        
        response = self.client.post(ref, {'email':'ainf23@mail.ru', 'password1':'Cjxb2014', 'password2':'Cjxb2014'})
        self.user_login()
        response = self.client.get(reverse('index'))
        self.assertContains(response, "No polls are available.")
        
        ClearModels()
    
    def test_authenticated_user(self):
        self.user_add()
        ret1 = create_question_choice("Who are you?", "Man")
        response = self.client.get(reverse('index'))         
        self.assertContains(response, "Man")
        response = self.client.post("/{}/".format(ret1[0].id))         
        self.assertNotContains(response, "100% Man")  
                
        response = self.client.post("/{}/".format(ret1[0].id), {'ch':ret1[1].id})         
        self.assertContains(response, "100% Man")      
        self.assertTrue(CUserChoice.objects.filter(choice = ret1[1]).exists())    
        response = self.client.get(reverse('index'))         
        self.assertContains(response, "No polls are available.")
        response = self.client.get(reverse('userresults'))         
        self.assertContains(response, "Choice: Man")
        
        response = self.client.get(reverse('detail',
                                   args=(ret1[0].id,)))
        self.assertContains(response, ret1[0].question_text,
                            status_code=200)
      
    
