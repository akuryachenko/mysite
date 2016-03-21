from django.test import TestCase
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.hashers import check_password
 
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
        
    
    def test_create_bad_super_user(self):
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
        
    def test_create_bad_user(self):
        with self.assertRaisesRegexp(ValueError, 'The given email must be set'): 
            create_user("",)
    
