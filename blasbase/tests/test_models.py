# -*- coding: utf-8 -*-
from django.test import TestCase

import datetime
from dateutil.relativedelta import relativedelta
from django.utils import timezone

from blasbase.models import *


class PersonMethodsTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        testFunktion = Function()
        testFunktion.name = "Trädgårdsmästare"
        testFunktion.engagement = True
        testFunktion.save()
        testFunktion2 = Function()
        testFunktion2.name = "Triangel"
        testFunktion2.membership = True
        testFunktion2.save()
        testFunktion3 = Function()
        testFunktion3.name = "bollkalle"
        testFunktion3.save()
        person = Person(first_name=u'Niklas', last_name=u'Namnlös')
        #måste lägga in en avatar
        person.save()


    def setUp(self):
        self.person = Person.objects.get(pk=1)


    def test_age_without_born_or_deceased(self):
        self.assertIsNone(self.person.age)

    def test_age_with_only_born(self):
        self.person.born = datetime.date.today() - datetime.timedelta(days=366)
        self.person.save()
        self.assertEqual(self.person.age, relativedelta(years=1, days=1))

    def test_age_with_only_deceased(self):
        self.person.deceased = datetime.date.today() - datetime.timedelta(days=1)
        self.person.save()
        self.assertIsNone(self.person.age)

    def test_age_with_born_and_deceased(self):
        self.person.born = datetime.date.today() - relativedelta(years=81)
        self.person.deceased = datetime.date.today() - relativedelta(years=1)
        self.person.save()
        self.assertEqual(self.person.age, relativedelta(years=80, months=0, days=0))

    """
    Måste lägga till en avatar i setup
    def test_primary_avatar(self):
        avatar = Avatar.objects.get(person=self.person, primary=True)
        self.assertEqual(self.person.primary_avatar, avatar)

    def test_secondary_avatars(self):
        avatars = Avatar.objects.filter(person=self.person).exclude(primary=True)
        self.assertItemsEqual(self.person.secondary_avatars, avatars)"""

    def test_full_name_without_nickname(self):
        self.person.first_name = 'First'
        self.person.last_name = 'Last'
        self.person.nickname = ''
        self.person.save()
        self.assertEqual(self.person.full_name, 'First Last')

    def test_full_name_with_nickname(self):
        self.person.first_name = 'First'
        self.person.last_name = 'Last'
        self.person.nickname = 'Nick'
        self.person.save()
        self.assertEqual(self.person.full_name, 'First "Nick" Last')

    def test_short_name_without_nickname(self):
        self.person.first_name = 'First'
        self.person.last_name = 'Last'
        self.person.nickname = ''
        self.person.save()
        self.assertEqual(self.person.short_name, 'First L')

    def test_short_name_with_nickname(self):
        self.person.first_name = 'First'
        self.person.last_name = 'Last'
        self.person.nickname = 'Nick'
        self.person.save()
        self.assertEqual(self.person.short_name, 'Nick')

    """    These needs to be looked into especially start_date and end_date

def test_start_date_with_non_member(self):

        Assignment.objects.create(person=self.person, function=Function.objects.get(name='bollkalle'),start=(datetime.date.today() - relativedelta(months=1)))
        self.assertIsNone(self.person.start_date)


    def test_start_date_with_trial_member(self):
        Assignment.objects.create(person=self.person, function=Function.objects.get(name='Triangel'), trial=True,
                                  start=(datetime.date.today() - relativedelta(months=1)))
        self.assertIsNone(self.person.start_date)

    def test_start_date_with_active_member(self):
        Assignment.objects.create(person=self.person, function=Function.objects.get(name='Triangel'),
                                  start=(datetime.date.today() - relativedelta(months=1)))
        self.assertEqual(self.person.start_date, (datetime.date.today() - relativedelta(months=1)))


    def test_start_date_with_oldie(self):
        Assignment.objects.create(person=self.person, function=Function.objects.get(name='Triangel'),
                                  start=(datetime.date.today() - relativedelta(years=10)),
                                  end=(datetime.date.today() - relativedelta(years=1)))
        self.assertEqual(self.person.start_date, (datetime.date.today() - relativedelta(years=10)))

    def test_start_date_with_returning_member(self):
        Assignment.objects.create(person=self.person, function=Function.objects.get(name='Triangel'),
                                  start=(datetime.date.today() - relativedelta(years=10)),
                                  end=(datetime.date.today() - relativedelta(years=3)))
        Assignment.objects.create(person=self.person, function=Function.objects.get(name='Triangel'),
                                  start=(datetime.date.today() - relativedelta(years=2)))
        self.assertEqual(self.person.start_date, (datetime.date.today() - relativedelta(years=10)))

    def test_end_date_with_non_member(self):
        Assignment.objects.create(person=self.person, function=Function.objects.get(name='bollkalle'),
                                  start=(datetime.date.today() - relativedelta(years=1)),
                                  end=(datetime.date.today() - relativedelta(months=1)))
        self.assertIsNone(self.person.end_date)

    def test_start_date_with_trial_member(self):
        Assignment.objects.create(person=self.person, function=Function.objects.get(name='Triangel'), trial=True,
                                  start=(datetime.date.today() - relativedelta(years=1)),
                                  end=(datetime.date.today() - relativedelta(months=1)))
        self.assertIsNone(self.person.start_date)

    def test_end_date_with_active_member(self):
        Assignment.objects.create(person=self.person, function=Function.objects.get(name='Triangel'),
                                  start=(datetime.date.today() - relativedelta(months=1)))
        self.assertIsNone(self.person.end_date)

    def test_end_date_with_oldie(self):
        Assignment.objects.create(person=self.person, function=Function.objects.get(name='Triangel'),
                                  start=(datetime.date.today() - relativedelta(years=10)),
                                  end=(datetime.date.today() - relativedelta(years=1)))
        self.assertEqual(self.person.end_date, (datetime.date.today() - relativedelta(years=1)))

    def test_assignments_returns_only_active(self):

        self.assertQuerysetEqual(self.person.assignments, )
"""