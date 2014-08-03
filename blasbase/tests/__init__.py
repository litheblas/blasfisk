# -*- coding: utf-8 -*-
from test_backends import *
from test_validators import *



from django.test import TestCase
from django.contrib.auth.models import Permission
from blasbase.models import Person, Function

import datetime
from dateutil.relativedelta import relativedelta


class BlasbaseTestCase(TestCase):
    def setUp(self):
        """
        Creates a few base objects. Creates no connections between objects, do that yourself in your test cases.
        """

        self.person_1 = Person.objects.create(first_name='Kim', last_name='Könsambivalent')
        self.person_2 = Person.objects.create(first_name='Niklas', last_name='Namnlös')
        self.person_3 = Person.objects.create(first_name='Anita', last_name='Anonym')
        self.people_set_1 = [self.person_1, self.person_2, self.person_3]

        self.function_1 = Function.objects.create(name='F 1')
        self.function_1_1 = Function.objects.create(name='F 1-1', parent=self.function_1)
        self.function_1_1_1 = Function.objects.create(name='F 1-1-1', parent=self.function_1_1)
        self.function_1_1_2 = Function.objects.create(name='F 1-1-2', parent=self.function_1_1)
        self.function_1_2 = Function.objects.create(name='F 1-2', parent=self.function_1)
        self.function_1_2_1 = Function.objects.create(name='F 1-2-1', parent=self.function_1_2)
        self.function_1_2_2 = Function.objects.create(name='F 1-2-2', parent=self.function_1_2)
        self.function_2 = Function.objects.create(name='F 2')
        self.function_2_1 = Function.objects.create(name='F 2-1', parent=self.function_2)
        self.function_2_1_1 = Function.objects.create(name='F 2-1-1', parent=self.function_2_1)
        self.function_2_1_2 = Function.objects.create(name='F 2-1-2', parent=self.function_2_1)
        self.function_2_2 = Function.objects.create(name='F 2-2', parent=self.function_2)
        self.function_2_2_1 = Function.objects.create(name='F 2-2-1', parent=self.function_2_2)
        self.function_2_2_2 = Function.objects.create(name='F 2-2-2', parent=self.function_2_2)

        # Damn ugly, but we don't care which permission object we get as long as we can reference it.
        self.permission_1 = Permission.objects.all()[0]
        self.permission_2 = Permission.objects.all()[1]
        self.permission_3 = Permission.objects.all()[2]
        self.permission_set_1 = [self.permission_1, self.permission_2, self.permission_3]

        self.date_today = datetime.date.today()
        self.date_more_past = self.date_today - relativedelta(years=2)
        self.date_past = self.date_today - relativedelta(years=1)
        self.date_future = self.date_today + relativedelta(years=1)
        self.date_more_future = self.date_today + relativedelta(years=2)

