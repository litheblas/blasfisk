# -*- coding: utf-8 -*-
import django_filters as filters


class PersonFilterSet(filters.FilterSet):
    class Meta:
        fields = [
            'name',
            'gender',
            'city',
            'country',
            'section',
            'post',
        ]