# -*- coding: utf-8 -*-
from pycountry import countries
import os.path
import uuid

def get_countries():
    c = []
    for country in countries:
        c.append((country.alpha2, country.name))
    return c

def generate_filename(instance, filename, location):
    extension = os.path.splitext(filename)[1].lower()
    
    # Döper filen till ett UUID eftersom vi inte ännu inte sparat objektet i databasen och därmed inte fått någon PK. Tror att det här borde funka tillräckligt bra. /Olle
    return os.path.join(location, str(uuid.uuid1()) + extension)  # Ger typ avatars/02b9672e-85f3-11e3-9e44-542696dae887.jpg

COUNTRIES = get_countries()

GENDERS = (
    ('f', 'Kvinna'),
    ('m', 'Man')
)