# -*- coding: utf-8 -*-

from blasbase.tests import BlasbaseTestCase
from blasbase.models import Assignment


class AssignmentMethodsTestCase(BlasbaseTestCase):
    def setUp(self):
        super(AssignmentMethodsTestCase, self).setUp()
        self.assignment_p_1_f_1 = Assignment.objects.create(person=self.person_1, function=self.function_1)

    def test_ongoing_no_start_no_end(self):
        self.assignment_p_1_f_1.start = None
        self.assignment_p_1_f_1.end = None

        self.assertFalse(self.assignment_p_1_f_1.ongoing)

    def test_ongoing_no_start_past_end(self):
        self.assignment_p_1_f_1.start = None
        self.assignment_p_1_f_1.end = self.date_past

        self.assertFalse(self.assignment_p_1_f_1.ongoing)

    def test_ongoing_no_start_today_end(self):
        self.assignment_p_1_f_1.start = None
        self.assignment_p_1_f_1.end = self.date_today

        self.assertTrue(self.assignment_p_1_f_1.ongoing)

    def test_ongoing_no_start_future_end(self):
        self.assignment_p_1_f_1.start = None
        self.assignment_p_1_f_1.end = self.date_future

        self.assertTrue(self.assignment_p_1_f_1.ongoing)

    def test_ongoing_past_start_no_end(self):
        self.assignment_p_1_f_1.start = self.date_past
        self.assignment_p_1_f_1.end = None

        self.assertTrue(self.assignment_p_1_f_1.ongoing)

    def test_ongoing_past_start_past_end(self):
        self.assignment_p_1_f_1.start = self.date_more_past
        self.assignment_p_1_f_1.end = self.date_past

        self.assertFalse(self.assignment_p_1_f_1.ongoing)

    def test_ongoing_past_start_today_end(self):
        self.assignment_p_1_f_1.start = self.date_past
        self.assignment_p_1_f_1.end = self.date_today

        self.assertTrue(self.assignment_p_1_f_1.ongoing)

    def test_ongoing_past_start_future_end(self):
        self.assignment_p_1_f_1.start = self.date_past
        self.assignment_p_1_f_1.end = self.date_future

        self.assertTrue(self.assignment_p_1_f_1.ongoing)

    def test_ongoing_today_start_no_end(self):
        self.assignment_p_1_f_1.start = self.date_today
        self.assignment_p_1_f_1.end = None

        self.assertTrue(self.assignment_p_1_f_1.ongoing)

    def test_ongoing_today_start_today_end(self):
        self.assignment_p_1_f_1.start = self.date_today
        self.assignment_p_1_f_1.end = self.date_today

        self.assertTrue(self.assignment_p_1_f_1.ongoing)

    def test_ongoing_today_start_future_end(self):
        self.assignment_p_1_f_1.start = self.date_today
        self.assignment_p_1_f_1.end = self.date_future

        self.assertTrue(self.assignment_p_1_f_1.ongoing)

    def test_ongoing_future_start_future_end(self):
        self.assignment_p_1_f_1.start = self.date_future
        self.assignment_p_1_f_1.end = self.date_more_future

        self.assertFalse(self.assignment_p_1_f_1.ongoing)


class AssignmentQuerySetSaneTestCase(BlasbaseTestCase):
    def setUp(self):
        super(AssignmentQuerySetSaneTestCase, self).setUp()
        self.assignment_p_1_f_1 = Assignment.objects.create(person=self.person_1, function=self.function_1)

    def test_sane_no_start_no_end(self):
        self.assignment_p_1_f_1.start = None
        self.assignment_p_1_f_1.end = None
        self.assignment_p_1_f_1.save()

        self.assertListEqual(list(Assignment.objects.sane()), [self.assignment_p_1_f_1])

    def test_sane_no_start_past_end(self):
        self.assignment_p_1_f_1.start = None
        self.assignment_p_1_f_1.end = self.date_past
        self.assignment_p_1_f_1.save()

        self.assertListEqual(list(Assignment.objects.sane()), [self.assignment_p_1_f_1])

    def test_sane_no_start_future_end(self):
        self.assignment_p_1_f_1.start = None
        self.assignment_p_1_f_1.end = self.date_future
        self.assignment_p_1_f_1.save()

        self.assertListEqual(list(Assignment.objects.sane()), [self.assignment_p_1_f_1])

    def test_sane_past_start_no_end(self):
        self.assignment_p_1_f_1.start = self.date_past
        self.assignment_p_1_f_1.end = None
        self.assignment_p_1_f_1.save()

        self.assertListEqual(list(Assignment.objects.sane()), [self.assignment_p_1_f_1])

    def test_sane_past_start_future_end(self):
        self.assignment_p_1_f_1.start = self.date_past
        self.assignment_p_1_f_1.end = self.date_future
        self.assignment_p_1_f_1.save()

        self.assertListEqual(list(Assignment.objects.sane()), [self.assignment_p_1_f_1])

    def test_sane_future_start_no_end(self):
        self.assignment_p_1_f_1.start = self.date_future
        self.assignment_p_1_f_1.end = None
        self.assignment_p_1_f_1.save()

        self.assertListEqual(list(Assignment.objects.sane()), [self.assignment_p_1_f_1])

    def test_sane_future_start_past_end(self):
        self.assignment_p_1_f_1.start = self.date_future
        self.assignment_p_1_f_1.end = self.date_past
        self.assignment_p_1_f_1.save()

        self.assertListEqual(list(Assignment.objects.sane()), [])

    def test_sane_same_start_end(self):
        self.assignment_p_1_f_1.start = self.date_today
        self.assignment_p_1_f_1.end = self.date_today
        self.assignment_p_1_f_1.save()

        self.assertListEqual(list(Assignment.objects.sane()), [self.assignment_p_1_f_1])


class AssignmentQuerySetDefinedTestCase(BlasbaseTestCase):
    def setUp(self):
        super(AssignmentQuerySetDefinedTestCase, self).setUp()
        self.assignment_p_1_f_1 = Assignment.objects.create(person=self.person_1, function=self.function_1)

    def test_defined_no_start_no_end(self):
        self.assignment_p_1_f_1.start = None
        self.assignment_p_1_f_1.end = None
        self.assignment_p_1_f_1.save()

        self.assertListEqual(list(Assignment.objects.defined()), [])

    def test_defined_no_start_past_end(self):
        self.assignment_p_1_f_1.start = None
        self.assignment_p_1_f_1.end = self.date_past
        self.assignment_p_1_f_1.save()

        self.assertListEqual(list(Assignment.objects.defined()), [self.assignment_p_1_f_1])

    def test_defined_no_start_future_end(self):
        self.assignment_p_1_f_1.start = None
        self.assignment_p_1_f_1.end = self.date_future
        self.assignment_p_1_f_1.save()

        self.assertListEqual(list(Assignment.objects.defined()), [self.assignment_p_1_f_1])

    def test_defined_past_start_no_end(self):
        self.assignment_p_1_f_1.start = self.date_past
        self.assignment_p_1_f_1.end = None
        self.assignment_p_1_f_1.save()

        self.assertListEqual(list(Assignment.objects.defined()), [self.assignment_p_1_f_1])

    def test_defined_past_start_future_end(self):
        self.assignment_p_1_f_1.start = self.date_past
        self.assignment_p_1_f_1.end = self.date_future
        self.assignment_p_1_f_1.save()

        self.assertListEqual(list(Assignment.objects.defined()), [self.assignment_p_1_f_1])

    def test_defined_future_start_no_end(self):
        self.assignment_p_1_f_1.start = self.date_future
        self.assignment_p_1_f_1.end = None
        self.assignment_p_1_f_1.save()

        self.assertListEqual(list(Assignment.objects.defined()), [self.assignment_p_1_f_1])

    def test_defined_future_start_past_end(self):
        self.assignment_p_1_f_1.start = self.date_future
        self.assignment_p_1_f_1.end = self.date_past
        self.assignment_p_1_f_1.save()

        self.assertListEqual(list(Assignment.objects.defined()), [self.assignment_p_1_f_1])

    def test_defined_same_start_end(self):
        self.assignment_p_1_f_1.start = self.date_today
        self.assignment_p_1_f_1.end = self.date_today
        self.assignment_p_1_f_1.save()

        self.assertListEqual(list(Assignment.objects.defined()), [self.assignment_p_1_f_1])


class AssignmentQuerySetOngoingTestCase(BlasbaseTestCase):
    def setUp(self):
        super(AssignmentQuerySetOngoingTestCase, self).setUp()
        self.assignment_p_1_f_1 = Assignment.objects.create(person=self.person_1, function=self.function_1)

    def test_ongoing_no_start_no_end(self):
        self.assignment_p_1_f_1.start = None
        self.assignment_p_1_f_1.end = None
        self.assignment_p_1_f_1.save()

        self.assertListEqual(list(Assignment.objects.ongoing()), [])

    def test_ongoing_no_start_past_end(self):
        self.assignment_p_1_f_1.start = None
        self.assignment_p_1_f_1.end = self.date_past
        self.assignment_p_1_f_1.save()

        self.assertListEqual(list(Assignment.objects.ongoing()), [])

    def test_ongoing_no_start_today_end(self):
        self.assignment_p_1_f_1.start = None
        self.assignment_p_1_f_1.end = self.date_today
        self.assignment_p_1_f_1.save()

        self.assertListEqual(list(Assignment.objects.ongoing()), [self.assignment_p_1_f_1])

    def test_ongoing_no_start_future_end(self):
        self.assignment_p_1_f_1.start = None
        self.assignment_p_1_f_1.end = self.date_future
        self.assignment_p_1_f_1.save()

        self.assertListEqual(list(Assignment.objects.ongoing()), [self.assignment_p_1_f_1])

    def test_ongoing_past_start_no_end(self):
        self.assignment_p_1_f_1.start = self.date_past
        self.assignment_p_1_f_1.end = None
        self.assignment_p_1_f_1.save()

        self.assertListEqual(list(Assignment.objects.ongoing()), [self.assignment_p_1_f_1])

    def test_ongoing_past_start_past_end(self):
        self.assignment_p_1_f_1.start = self.date_more_past
        self.assignment_p_1_f_1.end = self.date_past
        self.assignment_p_1_f_1.save()

        self.assertListEqual(list(Assignment.objects.ongoing()), [])

    def test_ongoing_past_start_today_end(self):
        self.assignment_p_1_f_1.start = self.date_past
        self.assignment_p_1_f_1.end = self.date_today
        self.assignment_p_1_f_1.save()

        self.assertListEqual(list(Assignment.objects.ongoing()), [self.assignment_p_1_f_1])

    def test_ongoing_past_start_future_end(self):
        self.assignment_p_1_f_1.start = self.date_past
        self.assignment_p_1_f_1.end = self.date_future
        self.assignment_p_1_f_1.save()

        self.assertListEqual(list(Assignment.objects.ongoing()), [self.assignment_p_1_f_1])

    def test_ongoing_today_start_no_end(self):
        self.assignment_p_1_f_1.start = self.date_today
        self.assignment_p_1_f_1.end = None
        self.assignment_p_1_f_1.save()

        self.assertListEqual(list(Assignment.objects.ongoing()), [self.assignment_p_1_f_1])

    def test_ongoing_today_start_today_end(self):
        self.assignment_p_1_f_1.start = self.date_today
        self.assignment_p_1_f_1.end = self.date_today
        self.assignment_p_1_f_1.save()

        self.assertListEqual(list(Assignment.objects.ongoing()), [self.assignment_p_1_f_1])

    def test_ongoing_today_start_future_end(self):
        self.assignment_p_1_f_1.start = self.date_today
        self.assignment_p_1_f_1.end = self.date_future
        self.assignment_p_1_f_1.save()

        self.assertListEqual(list(Assignment.objects.ongoing()), [self.assignment_p_1_f_1])

    def test_ongoing_future_start_future_end(self):
        self.assignment_p_1_f_1.start = self.date_future
        self.assignment_p_1_f_1.end = self.date_more_future
        self.assignment_p_1_f_1.save()

        self.assertListEqual(list(Assignment.objects.ongoing()), [])


class AssignmentQuerySetEndedTestCase(BlasbaseTestCase):
    def setUp(self):
        super(AssignmentQuerySetEndedTestCase, self).setUp()
        self.assignment_p_1_f_1 = Assignment.objects.create(person=self.person_1, function=self.function_1)

    def test_ended_no_start_no_end(self):
        self.assignment_p_1_f_1.start = None
        self.assignment_p_1_f_1.end = None
        self.assignment_p_1_f_1.save()

        self.assertListEqual(list(Assignment.objects.ended()), [self.assignment_p_1_f_1])

    def test_ended_no_start_past_end(self):
        self.assignment_p_1_f_1.start = None
        self.assignment_p_1_f_1.end = self.date_past
        self.assignment_p_1_f_1.save()

        self.assertListEqual(list(Assignment.objects.ended()), [self.assignment_p_1_f_1])

    def test_ended_no_start_today_end(self):
        self.assignment_p_1_f_1.start = None
        self.assignment_p_1_f_1.end = self.date_today
        self.assignment_p_1_f_1.save()

        self.assertListEqual(list(Assignment.objects.ended()), [])

    def test_ended_no_start_future_end(self):
        self.assignment_p_1_f_1.start = None
        self.assignment_p_1_f_1.end = self.date_future
        self.assignment_p_1_f_1.save()

        self.assertListEqual(list(Assignment.objects.ended()), [])

    def test_ended_past_start_no_end(self):
        self.assignment_p_1_f_1.start = self.date_past
        self.assignment_p_1_f_1.end = None
        self.assignment_p_1_f_1.save()

        self.assertListEqual(list(Assignment.objects.ended()), [])

    def test_ended_past_start_past_end(self):
        self.assignment_p_1_f_1.start = self.date_more_past
        self.assignment_p_1_f_1.end = self.date_past
        self.assignment_p_1_f_1.save()

        self.assertListEqual(list(Assignment.objects.ended()), [self.assignment_p_1_f_1])

    def test_ended_past_start_today_end(self):
        self.assignment_p_1_f_1.start = self.date_past
        self.assignment_p_1_f_1.end = self.date_today
        self.assignment_p_1_f_1.save()

        self.assertListEqual(list(Assignment.objects.ended()), [])

    def test_ended_past_start_future_end(self):
        self.assignment_p_1_f_1.start = self.date_past
        self.assignment_p_1_f_1.end = self.date_future
        self.assignment_p_1_f_1.save()

        self.assertListEqual(list(Assignment.objects.ended()), [])

    def test_ended_today_start_no_end(self):
        self.assignment_p_1_f_1.start = self.date_today
        self.assignment_p_1_f_1.end = None
        self.assignment_p_1_f_1.save()

        self.assertListEqual(list(Assignment.objects.ended()), [])

    def test_ended_today_start_today_end(self):
        self.assignment_p_1_f_1.start = self.date_today
        self.assignment_p_1_f_1.end = self.date_today
        self.assignment_p_1_f_1.save()

        self.assertListEqual(list(Assignment.objects.ended()), [])

    def test_ended_today_start_future_end(self):
        self.assignment_p_1_f_1.start = self.date_today
        self.assignment_p_1_f_1.end = self.date_future
        self.assignment_p_1_f_1.save()

        self.assertListEqual(list(Assignment.objects.ended()), [])

    def test_ended_future_start_future_end(self):
        self.assignment_p_1_f_1.start = self.date_future
        self.assignment_p_1_f_1.end = self.date_more_future
        self.assignment_p_1_f_1.save()

        self.assertListEqual(list(Assignment.objects.ended()), [])


class AssignmentQuerySetMembershipsTestCase(BlasbaseTestCase):
    def setUp(self):
        super(AssignmentQuerySetMembershipsTestCase, self).setUp()
        self.assignment_p_1_f_1 = Assignment.objects.create(person=self.person_1, function=self.function_1)

    def test_memberships_mem_false(self):
        self.assignment_p_1_f_1.function.membership = False
        self.assignment_p_1_f_1.function.save()

        self.assertListEqual(list(Assignment.objects.memberships(all=False)), [])

    def test_memberships_mem_true(self):
        self.assignment_p_1_f_1.function.membership = True
        self.assignment_p_1_f_1.function.save()

        self.assertListEqual(list(Assignment.objects.memberships(all=False)), [self.assignment_p_1_f_1])

    def test_memberships_mem_true_trial(self):
        self.assignment_p_1_f_1.function.membership = True
        self.assignment_p_1_f_1.function.save()
        self.assignment_p_1_f_1.trial = True
        self.assignment_p_1_f_1.save()

        self.assertListEqual(list(Assignment.objects.memberships(all=False)), [])

    def test_memberships_eng_false(self):
        self.assignment_p_1_f_1.function.engagement = False
        self.assignment_p_1_f_1.function.save()

        self.assertListEqual(list(Assignment.objects.memberships(all=False)), [])

    def test_memberships_eng_true(self):
        self.assignment_p_1_f_1.function.engagement = True
        self.assignment_p_1_f_1.function.save()

        self.assertListEqual(list(Assignment.objects.memberships(all=False)), [])

    def test_memberships_eng_true_trial(self):
        self.assignment_p_1_f_1.function.engagement = True
        self.assignment_p_1_f_1.function.save()
        self.assignment_p_1_f_1.trial = True
        self.assignment_p_1_f_1.save()

        self.assertListEqual(list(Assignment.objects.memberships(all=False)), [])

    def test_memberships_all_mem_false(self):
        self.assignment_p_1_f_1.function.membership = False
        self.assignment_p_1_f_1.function.save()

        self.assertListEqual(list(Assignment.objects.memberships(all=True)), [])

    def test_memberships_all_mem_true(self):
        self.assignment_p_1_f_1.function.membership = True
        self.assignment_p_1_f_1.function.save()

        self.assertListEqual(list(Assignment.objects.memberships(all=True)), [self.assignment_p_1_f_1])

    def test_memberships_all_mem_true_trial(self):
        self.assignment_p_1_f_1.function.membership = True
        self.assignment_p_1_f_1.function.save()
        self.assignment_p_1_f_1.trial = True
        self.assignment_p_1_f_1.save()

        self.assertListEqual(list(Assignment.objects.memberships(all=True)), [self.assignment_p_1_f_1])

    def test_memberships_all_eng_false(self):
        self.assignment_p_1_f_1.function.engagement = False
        self.assignment_p_1_f_1.function.save()

        self.assertListEqual(list(Assignment.objects.memberships(all=True)), [])

    def test_memberships_all_eng_true(self):
        self.assignment_p_1_f_1.function.engagement = True
        self.assignment_p_1_f_1.function.save()

        self.assertListEqual(list(Assignment.objects.memberships(all=True)), [])

    def test_memberships_all_eng_true_trial(self):
        self.assignment_p_1_f_1.function.engagement = True
        self.assignment_p_1_f_1.function.save()
        self.assignment_p_1_f_1.trial = True
        self.assignment_p_1_f_1.save()

        self.assertListEqual(list(Assignment.objects.memberships(all=True)), [])
