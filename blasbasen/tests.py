# -*- coding: utf-8 -*-
from django.test import TestCase

import datetime
from django.utils import timezone


from blasbasen.models import *

def setup():
    Section.objects.create(name='Sektion 1', 
                           description='Det här är sektion 1')
    Section.objects.create(name='Sektion 2', 
                           description='Det här är sektion 2')
    Section.objects.create(name='Sektion 3', 
                           description='Det här är sektion 3')
    
    Post.objects.create(section=Section.objects.get(id=1),
                        name='Post 1', 
                        description='Det här är post 1', 
                        membership=False, 
                        engagement=False, 
                        show_in_timeline=False)
    Post.objects.create(section=Section.objects.get(id=1),
                        name='Post 2', 
                        description='Det här är post 2', 
                        membership=False, 
                        engagement=True, 
                        show_in_timeline=False)
    Post.objects.create(section=Section.objects.get(id=2),
                        name='Post 3', 
                        description='Det här är post 3', 
                        membership=False, 
                        engagement=True, 
                        show_in_timeline=True)
    Post.objects.create(section=Section.objects.get(id=2),
                        name='Post 4', 
                        description='Det här är post 4', 
                        membership=True, 
                        engagement=False, 
                        show_in_timeline=False)
    Post.objects.create(section=Section.objects.get(id=3),
                        name='Post 5', 
                        description='Det här är post 5', 
                        membership=True, 
                        engagement=False, 
                        show_in_timeline=True)
    Post.objects.create(section=Section.objects.get(id=3),
                        name='Post 6', 
                        description='Det här är post 6', 
                        membership=True, 
                        engagement=True, 
                        show_in_timeline=False)
    Post.objects.create(section=Section.objects.get(id=3),
                        name='Post 7', 
                        description='Det här är post 7', 
                        membership=True, 
                        engagement=True, 
                        show_in_timeline=True)
    
    
    
    Person.objects.create(first_name='Chuck',
                          nickname='NOPE',
                          last_name='Testa',
                          born=timezone.now() - datetime.timedelta(days=50*365),
                          deceased=timezone.now() - datetime.timedelta(days=10),
                          personal_id_number='1234',
                          liu_id='chute123',
                          address='Road street 671',
                          postcode='12345',
                          city='Ojai Valley',
                          country='US',
                          about='I specialize in the most lifelike dead animals anywhere. Period.')
    Person.objects.create(first_name='Lasse',
                          nickname='Hasse Lolm',
                          last_name='Holm',
                          born=timezone.now() - datetime.timedelta(days=40*365),
                          deceased=None,
                          personal_id_number='1234',
                          liu_id='hasho123',
                          address='Gatvägen 1',
                          postcode='12345',
                          city='Stockholm',
                          country='SE',
                          about='Jag blir fascinerad.')
    Person.objects.create(first_name='Chuck',
                          nickname='NOPE',
                          last_name='Testa',
                          born=timezone.now() - datetime.timedelta(days=50*365),
                          deceased=timezone.now() - datetime.timedelta(days=10),
                          personal_id_number='1234',
                          liu_id='chute123',
                          address='Road street 671',
                          postcode='12345',
                          city='Ojai Valley',
                          country='US',
                          about='I specialize in the most lifelike dead animals anywhere. Period.')

class PersonTestCase(TestCase):
    def __init__(self):
        setup()