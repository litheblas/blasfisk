# -*- coding: utf-8 -*-
from django.test import TestCase

import datetime
from django.utils import timezone
from django.core.exceptions import ValidationError

from blasbase import validators

class ValidatorTestCase(TestCase):
    def test_datetime_before_datetime_with_relative_future_datetime(self):
        date1 = timezone.now() - datetime.timedelta(seconds=1)
        date2 = timezone.now() + datetime.timedelta(seconds=1)
        self.assertIsNone(validators.datetime_before_datetime(date1, date2, 'Dummy message'))
        
    def test_datetime_before_datetime_with_relative_past_datetime(self):
        date1 = timezone.now() + datetime.timedelta(seconds=1)
        date2 = timezone.now() - datetime.timedelta(seconds=1)
        self.assertRaises(ValidationError, validators.datetime_before_datetime, date1, date2, 'Dummy message')
        
    def test_datetime_before_datetime_with_same_datetime(self):
        date1 = timezone.now()
        date2 = date1
        self.assertIsNone(validators.datetime_before_datetime(date1, date2, 'Dummy message'))
    
    def test_datetime_before_datetime_with_empty_datetime_one(self):
        date1 = None
        date2 = timezone.now()
        self.assertIsNone(validators.datetime_before_datetime(date1, date2, 'Dummy message'))
    
    def test_datetime_before_datetime_with_empty_datetime_two(self):
        date1 = timezone.now()
        date2 = None
        self.assertIsNone(validators.datetime_before_datetime(date1, date2, 'Dummy message'))
        
    def test_datetime_before_datetime_with_relative_future_date(self):
        date1 = datetime.date.today() - datetime.timedelta(days=1)
        date2 = datetime.date.today() + datetime.timedelta(days=1)
        self.assertIsNone(validators.datetime_before_datetime(date1, date2, 'Dummy message'))
        
    def test_datetime_before_datetime_with_relative_past_date(self):
        date1 = datetime.date.today() + datetime.timedelta(days=1)
        date2 = datetime.date.today() - datetime.timedelta(days=1)
        self.assertRaises(ValidationError, validators.datetime_before_datetime, date1, date2, 'Dummy message')
        
    def test_datetime_before_datetime_with_same_date(self):
        date1 = datetime.date.today()
        date2 = date1
        self.assertIsNone(validators.datetime_before_datetime(date1, date2, 'Dummy message'))
    
    def test_datetime_before_datetime_with_empty_date_one(self):
        date1 = None
        date2 = datetime.date.today()
        self.assertIsNone(validators.datetime_before_datetime(date1, date2, 'Dummy message'))
    
    def test_datetime_before_datetime_with_empty_date_two(self):
        date1 = datetime.date.today()
        date2 = None
        self.assertIsNone(validators.datetime_before_datetime(date1, date2, 'Dummy message'))