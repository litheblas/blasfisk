# -*- coding: utf-8 -*-
from django import forms
from blasbasen.models import Person, User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

# Från http://www.caktusgroup.com/blog/2013/08/07/migrating-custom-user-model-django/
# appname/forms.py
class BlasUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """

    def __init__(self, *args, **kargs):
        super(BlasUserCreationForm, self).__init__(*args, **kargs)
        del self.fields['email', 'first_name', 'last_name']

    class Meta:
        model = User
        fields = ('username',)

class BlasUserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __init__(self, *args, **kargs):
        super(BlasUserChangeForm, self).__init__(*args, **kargs)
        #del self.fields['username']

    class Meta:
        model = User