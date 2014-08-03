# -*- coding: utf-8 -*-

from blasbase.tests import BlasbaseTestCase
from blasbase.models import *


class PersonMethodsTestCase(BlasbaseTestCase):
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


    def test_age_without_born_or_deceased(self):
        self.person_1.born = None
        self.person_1.deceased = None

        self.assertIsNone(self.person_1.age)

    def test_age_with_only_born(self):
        self.person_1.born = datetime.date.today() - datetime.timedelta(days=366)
        self.person_1.deceased = None

        self.assertEqual(self.person_1.age, relativedelta(years=1, days=1))

    def test_age_with_only_deceased(self):
        self.person_1.born = None
        self.person_1.deceased = datetime.date.today() - datetime.timedelta(days=1)

        self.assertIsNone(self.person_1.age)

    def test_age_with_born_and_deceased(self):
        self.person_1.born = datetime.date.today() - relativedelta(years=81)
        self.person_1.deceased = datetime.date.today() - relativedelta(years=1)

        self.assertEqual(self.person_1.age, relativedelta(years=80, months=0, days=0))

    """
    Måste lägga till en avatar i setup
    def test_primary_avatar(self):
        avatar = Avatar.objects.get(person_1=self.person_1, primary=True)
        self.assertEqual(self.person_1.primary_avatar, avatar)

    def test_secondary_avatars(self):
        avatars = Avatar.objects.filter(person_1=self.person_1).exclude(primary=True)
        self.assertItemsEqual(self.person_1.secondary_avatars, avatars)"""

    def test_short_name_without_nickname(self):
        self.person_1.first_name = 'First'
        self.person_1.last_name = 'Last'
        self.person_1.nickname = ''

        self.assertEqual(self.person_1.short_name, 'First L')

    def test_short_name_with_nickname(self):
        self.person_1.first_name = 'First'
        self.person_1.last_name = 'Last'
        self.person_1.nickname = 'Nick'

        self.assertEqual(self.person_1.short_name, 'Nick')

    def test_full_name_without_nickname(self):
        self.person_1.first_name = 'First'
        self.person_1.last_name = 'Last'
        self.person_1.nickname = ''

        self.assertEqual(self.person_1.full_name, 'First Last')

    def test_full_name_with_nickname(self):
        self.person_1.first_name = 'First'
        self.person_1.last_name = 'Last'
        self.person_1.nickname = 'Nick'

        self.assertEqual(self.person_1.full_name, 'First "Nick" Last')

class PersonManagerMethodsTestCase(BlasbaseTestCase):
    pass





    """    These needs to be looked into especially membership_start and membership_end

def test_start_date_with_non_member(self):

        Assignment.objects.create(person_1=self.person_1, function=Function.objects.get(name='bollkalle'),start=(datetime.date.today() - relativedelta(months=1)))
        self.assertIsNone(self.person_1.membership_start)


    def test_start_date_with_trial_member(self):
        Assignment.objects.create(person_1=self.person_1, function=Function.objects.get(name='Triangel'), trial=True,
                                  start=(datetime.date.today() - relativedelta(months=1)))
        self.assertIsNone(self.person_1.membership_start)

    def test_start_date_with_active_member(self):
        Assignment.objects.create(person_1=self.person_1, function=Function.objects.get(name='Triangel'),
                                  start=(datetime.date.today() - relativedelta(months=1)))
        self.assertEqual(self.person_1.membership_start, (datetime.date.today() - relativedelta(months=1)))


    def test_start_date_with_oldie(self):
        Assignment.objects.create(person_1=self.person_1, function=Function.objects.get(name='Triangel'),
                                  start=(datetime.date.today() - relativedelta(years=10)),
                                  end=(datetime.date.today() - relativedelta(years=1)))
        self.assertEqual(self.person_1.membership_start, (datetime.date.today() - relativedelta(years=10)))

    def test_start_date_with_returning_member(self):
        Assignment.objects.create(person_1=self.person_1, function=Function.objects.get(name='Triangel'),
                                  start=(datetime.date.today() - relativedelta(years=10)),
                                  end=(datetime.date.today() - relativedelta(years=3)))
        Assignment.objects.create(person_1=self.person_1, function=Function.objects.get(name='Triangel'),
                                  start=(datetime.date.today() - relativedelta(years=2)))
        self.assertEqual(self.person_1.membership_start, (datetime.date.today() - relativedelta(years=10)))

    def test_end_date_with_non_member(self):
        Assignment.objects.create(person_1=self.person_1, function=Function.objects.get(name='bollkalle'),
                                  start=(datetime.date.today() - relativedelta(years=1)),
                                  end=(datetime.date.today() - relativedelta(months=1)))
        self.assertIsNone(self.person_1.membership_end)

    def test_start_date_with_trial_member(self):
        Assignment.objects.create(person_1=self.person_1, function=Function.objects.get(name='Triangel'), trial=True,
                                  start=(datetime.date.today() - relativedelta(years=1)),
                                  end=(datetime.date.today() - relativedelta(months=1)))
        self.assertIsNone(self.person_1.membership_start)

    def test_end_date_with_active_member(self):
        Assignment.objects.create(person_1=self.person_1, function=Function.objects.get(name='Triangel'),
                                  start=(datetime.date.today() - relativedelta(months=1)))
        self.assertIsNone(self.person_1.membership_end)

    def test_end_date_with_oldie(self):
        Assignment.objects.create(person_1=self.person_1, function=Function.objects.get(name='Triangel'),
                                  start=(datetime.date.today() - relativedelta(years=10)),
                                  end=(datetime.date.today() - relativedelta(years=1)))
        self.assertEqual(self.person_1.membership_end, (datetime.date.today() - relativedelta(years=1)))

    def test_assignments_returns_only_active(self):

        self.assertQuerysetEqual(self.person_1.assignments, )
"""