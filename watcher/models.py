# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import Group

class Watcher(models.Model):
    """Lägger automatiskt till användare till en grupp och/eller mailinglista baserat på sektion eller post."""
    #Leta i
    sections = models.ManyToManyField('blasbasen.Section', blank=True, null=True)
    posts = models.ManyToManyField('blasbasen.Post', blank=True, null=True)
     
    #Lägg till i
    group = models.ForeignKey(Group)
    list = models.ForeignKey('mailing.MailingList')
     
    def apply(self):
        #TODO: Allt
        
        pass