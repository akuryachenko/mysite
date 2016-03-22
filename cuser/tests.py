from django.test import TestCase, Client
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.core.signing import Signer
from django import forms 
from django.core.urlresolvers import reverse
import datetime
from django.template.loader import render_to_string
from django.contrib.sessions.models import Session

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
        
        ClearModels()
        
    def test_create_user_user_none_email(self):
        with self.assertRaisesRegexp(ValueError, 'The given email must be set'): 
            create_user("",)
    

class CUserTests(TestCase):
    
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
        sign = signer.sign("ainf23@mail.ru")
        
        self.assertRegexpMatches(ref, sign)
                
        response = self.client.post(ref, {'email':'ainf23@mail.ru', 'password1':'222', 'password2':'222'})
           
        log = self.client.login(username='ainf23@mail.ru', password='222')
        self.assertTrue(log)
        
        ClearModels()

    def test_registration_and_confirm_active_user(self):
        response = self.client.post('/registration/', {'email':'ainf23@mail.ru'})
        ref = response.context['reference']
        response = self.client.post(ref, {'email':'ainf23@mail.ru', 'password1':'222', 'password2':'222'})
        
        response = self.client.post(ref, {'email':'ainf23@mail.ru', 'password1':'222', 'password2':'222'})
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
        
    def test_registration_and_confirm_user_bad_refference (self):
        response = self.client.post('/registration/', {'email':'ainf23@mail.ru'})
        ref = response.context['reference']
        ref = ref.replace("ainf23@mail.ru","ainf24@mail.ru")
        response = self.client.post(ref, {'email':'ainf24@mail.ru', 'password1':'222', 'password2':'222'})
        self.assertEqual(response.status_code, 404)        
        
        log = self.client.login(username='ainf24@mail.ru', password='222')
        self.assertEqual(log, False)
        
        ClearModels()
        
 
def create_question_choice(question_text, choice_text):   
    question  = Question.objects.create(question_text=question_text, pub_date=timezone.now())
    choice = Choice.objects.create(question = question, choice_text = choice_text)
    return (question, choice)


class VoteTests(TestCase):
    
    def test_vote_anonymous_user(self):
        ret = create_question_choice("Who are you?", "Man")
        response = self.client.post("/{}/".format(ret[0].id), kwargs={'ch':ret[1].id})
        self.assertContains(response, "In order to vote you must register")
        
        session = self.client.session
        session['anonym_vote'] = ret[1].id
        session.save()
           
        self.client.post('/registration/', {'email':'ainf23@mail.ru'})
        self.assertTrue(CUserChoice.objects.filter(choice = ret[1]).exists())            
        
        ClearModels()
        
class ResultsTests(TestCase):        
    def test_anonymous_user(self):
        ret = create_question_choice("Who are you?", "Man")
        response = self.client.post(reverse('results', args=(ret[0].id,)))
        self.assertEqual(response.status_code, 404)        
        ClearModels()
        
    def test_authenticated_user(self):
        
        ret = create_question_choice("Who are you?", "Man")
                
        response = self.client.post('/registration/', {'email':'ainf23@mail.ru'})
        self.assertIn('reference',response.context)
        ref = response.context['reference']
        response = self.client.post(ref, {'email':'ainf23@mail.ru', 'password1':'222', 'password2':'222'})
        self.client.login(username='ainf23@mail.ru', password='222')
         
        response = self.client.post(reverse('results', args=(ret[0].id,)))
        self.assertEqual(response.status_code, 405)       
        
        ClearModels()
        
        
    
        
class IndexTests(TestCase):
    
    def test_authenticated_user(self):
        
        ret1 = create_question_choice("Who are you?", "Man")
        ret2 = create_question_choice("Your favorite Beatles?", "Jon")
        
        response = self.client.post('/registration/', {'email':'ainf23@mail.ru'})
        self.assertIn('reference',response.context)
        ref = response.context['reference']
        response = self.client.post(ref, {'email':'ainf23@mail.ru', 'password1':'222', 'password2':'222'})
        self.client.login(username='ainf23@mail.ru', password='222')
         
        response = self.client.get(reverse('index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Your favorite Beatles?>', '<Question: Who are you?>']
        ) 
                     
        #response = self.client.post("/{}/".format(ret1[0].id), kwargs={'ch':ret1[1].id})
        response = self.client.post("/{}/".format(ret1[0].id), {'ch': 1})
               
        response = self.client.get(reverse('index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Your favorite Beatles?>']
        )
        
        ClearModels()
        
      
      
