# -*- coding: utf-8 -*-
from pycountry import countries

def get_countries():
    c = []
    for country in countries:
        c.append((country.alpha2, country.name))
    return c

COUNTRIES = get_countries()

GENDERS = (
    ('f', 'Kvinna'),
    ('m', 'Man')
)