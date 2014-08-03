# -*- coding: utf-8 -*-

from django.test import TestCase
from blasbase.models import *
from django.contrib.auth.models import Permission

class BlasbaseBackendTestCase(TestCase):
    def setUp(self):
        self.person_1 = Person.objects.create(first_name='Niklas', last_name='Namnlös')

        self.function_1 = Function.objects.create(name='F 1')
        self.function_1_1 = Function.objects.create(name='F 1-1', parent=self.function_1)
        self.function_1_1_1 = Function.objects.create(name='F 1-1-1', parent=self.function_1_1)
        self.function_1_1_2 = Function.objects.create(name='F 1-1-2', parent=self.function_1_1)
        self.function_1_2 = Function.objects.create(name='F 1-2', parent=self.function_1)
        self.function_1_2_1 = Function.objects.create(name='F 1-2-1', parent=self.function_1_2)

        # Damn ugly, but we don't care which permission object we get as long as we can reference it.
        self.permission_1 = Permission.objects.all()[0]
        self.permission_2 = Permission.objects.all()[1]
        self.permission_3 = Permission.objects.all()[2]

    def test_has_perm_tries_all_permissions(self):
        assert False

    def test_has_perm_inherited_from_direct_parent(self):
        assert False

    def test_has_perm_inherited_from_indirect_parent(self):
        assert False

    def test_has_perm_not_inherited_from_sibling(self):
        assert False

    def test_has_perm_not_inherited_from_direct_child(self):
        assert False

    def test_has_perm_not_inherited_from_indirect_child(self):
        assert False

    def test_has_perm_assignment_past_start_past_end(self):
        assert False

    def test_has_perm_assignment_past_start_no_end(self):
        assert False

    def test_has_perm_assignment_past_start_today_end(self):
        assert False

    def test_has_perm_assignment_past_start_future_end(self):
        assert False

    def test_has_perm_assignment_no_start_past_end(self):
        assert False

    def test_has_perm_assignment_no_start_no_end(self):
        assert False

    def test_has_perm_assignment_no_start_today_end(self):
        assert False

    def test_has_perm_assignment_no_start_future_end(self):
        assert False

    def test_has_perm_assignment_today_start_today_end(self):
        assert False

    def test_has_perm_assignment_today_start_no_end(self):
        assert False

    def test_has_perm_assignment_today_start_future_end(self):
        assert False

    def test_has_perm_assignment_future_start_future_end(self):
        assert False