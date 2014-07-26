# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import Group
from django.utils.encoding import python_2_unicode_compatible

answers = (
    ('No', 'Nej'),
    ('Maybe', 'Kanske'), # TODO: Ska vi ha ett sånt här alternativ?
    ('Yes', 'Ja'),
)


@python_2_unicode_compatible
class EventType(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Attendance(models.Model):
    #Skapas när användaren bjuds in till eller själv går med i ett evenemang
    event = models.ForeignKey('Event')
    person = models.ForeignKey('blasbase.Person')
    
    answer = models.CharField(max_length=8, choices=answers, blank=True) # Blank = inget svar

@python_2_unicode_compatible
class Event(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    type = models.ForeignKey(EventType)
    public = models.BooleanField()
    attendees = models.ManyToManyField('blasbase.Person', through=Attendance)
    
    customer = models.ForeignKey('blasbase.Customer')
    price = models.DecimalField(max_digits=10, decimal_places=2)


@python_2_unicode_compatible
class TargetedInfo(models.Model):
    event = models.ForeignKey(Event)
    group = models.ForeignKey(Group)
    content = models.TextField()
