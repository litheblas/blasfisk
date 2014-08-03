# -*- coding: utf-8 -*-

from blasbase.tests import BlasbaseTestCase
from blasbase.models import Assignment


class FunctionMethodsTestCase(BlasbaseTestCase):
    def test_inherited_permissions_directly_assigned(self):
        self.function_1.permissions = self.permission_set_1

        self.assertListEqual(list(self.function_1.inherited_permissions), self.permission_set_1)

    def test_inherited_permissions_inherited_from_direct_parent(self):
        self.function_1.permissions = self.permission_set_1

        self.assertListEqual(list(self.function_1_1.inherited_permissions), self.permission_set_1)

    def test_inherited_permissions_inherited_from_indirect_parent(self):
        self.function_1.permissions = self.permission_set_1

        self.assertListEqual(list(self.function_1_1_1.inherited_permissions), self.permission_set_1)

    def test_inherited_permissions_not_inherited_from_sibling(self):
        self.function_1.permissions = self.permission_set_1

        self.assertListEqual(list(self.function_2.inherited_permissions), [])

    def test_inherited_permissions_not_inherited_from_direct_child(self):
        self.function_1_1.permissions = self.permission_set_1

        self.assertListEqual(list(self.function_1.inherited_permissions), [])

    def test_inherited_permissions_not_inherited_from_indirect_child(self):
        self.function_1_1_1.permissions = self.permission_set_1

        self.assertListEqual(list(self.function_1.inherited_permissions), [])

    def test_people_directly_assigned(self):
        assignment = Assignment.objects.create(person=self.person_1, function=self.function_1)

        self.assertListEqual(list(self.function_1.people), [assignment.person])

    def test_people_inherited_from_direct_child(self):
        assignment = Assignment.objects.create(person=self.person_1, function=self.function_1_1)

        self.assertListEqual(list(self.function_1.people), [assignment.person])

    def test_people_inherited_from_indirect_child(self):
        assignment = Assignment.objects.create(person=self.person_1, function=self.function_1_1_1)

        self.assertListEqual(list(self.function_1.people), [assignment.person])

    def test_people_not_inherited_from_sibling(self):
        assignment = Assignment.objects.create(person=self.person_1, function=self.function_2)

        self.assertListEqual(list(self.function_1.people), [])

    def test_people_not_inherited_from_direct_parent(self):
        assignment = Assignment.objects.create(person=self.person_1, function=self.function_1)

        self.assertListEqual(list(self.function_1_1.people), [])

    def test_people_not_inherited_from_indirect_parent(self):
        assignment = Assignment.objects.create(person=self.person_1, function=self.function_1)

        self.assertListEqual(list(self.function_1_1_1.people), [])