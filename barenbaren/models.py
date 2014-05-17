# -*- coding: utf-8 -*-
from django.db import models

#class Event(models.Model):
#    pass

class Balance(models.Model):
    person = models.OneToOneField('blasbasen.Person')
    balance = models.DecimalField(max_digits=9, decimal_places=2)
    
    def __unicode__(self):
        return u'{0}: {1}'.format(self.person.get_short_name(), self.balance)

class Consumption(models.Model):
    """Knyter samman användare, evenemang, dag och streck"""
    event_person = models.ForeignKey('events.Attendance', null=True, blank=True)
    date = models.DateField()
    amount = models.PositiveIntegerField()
    
    class Meta:
        unique_together = [['event_person', 'date'],]
    
    def __unicode__(self):
        return u'{0}: {1}, {2} cl'.format(self.date, self.event_person, self.amount)