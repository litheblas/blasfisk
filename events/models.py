# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import Group
from litheblas.blasbasen.models import User, Customer

answers = (
    ('No', 'Nej'),
    ('Maybe', 'Kanske'), # TODO: Ska vi ha ett sånt här alternativ?
    ('Yes', 'Ja'),
)

class EventType(models.Model):
    name = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.name
    
class Attendance(models.Model):
    #Skapas när användaren bjuds in till eller själv går med i ett evenemang
    event = models.ForeignKey('Event')
    user = models.ForeignKey(User)
    
    answer = models.CharField(max_length=8, choices=answers, blank=True) # Blank = inget svar

class Event(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    type = models.ForeignKey(EventType)
    attendees = models.ManyToManyField(User, through=Attendance)
    
    customer = models.ForeignKey(Customer)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
class TargetedInfo(models.Model):
    event = models.ForeignKey(Event)
    group = models.ForeignKey(Group)
    content = models.TextField()