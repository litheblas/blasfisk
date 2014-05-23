# -*- coding: utf-8 -*-
from django import forms
from blasbasen.models import Person

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person