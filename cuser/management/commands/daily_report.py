from __future__ import unicode_literals
from itertools import count
from datetime import datetime, timedelta
from io import BytesIO

from django.conf import settings
from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _, activate, deactivate

from polls.models import Choice, Question, CUserChoice
from .models import CUser


class Command(BaseCommand):
    
    #===========================================================================
    # Handle
    #===========================================================================

    def handle(self, *args, **options):
        orders = Order.objects.filter(is_processed=False, type='order', billing_address__country='IT').\
            select_related('billing_address', 'shipping_address').\
            select_for_update()
        if not orders.exists():
            return
        
        activate('it')
        self.prepare_email(orders)
        self.prepare_shopify_order(orders)
        orders.update(is_processed=True)
        deactivate()
