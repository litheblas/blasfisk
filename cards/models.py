# -*- coding: utf-8 -*-
from django.db import models
from litheblas.blasbasen.models import User



class Card(models.Model):
    enabled = models.BooleanField(default=True) #Sätt till False istället för att ta bort, så bevaras historiken.
    card_data = models.CharField(max_length=256) #TODO: Kolla exakt vad av kortets data som läses av. Vad av detta skall lagras?
    user = models.ForeignKey(User) #Kort _måste_ associeras med en användare. Låt det vara så så slipper vi vilsna kort som ingen vet vem de tillhör.
    
    def __unicode__(self):
        return '{0} ({1})'.format(self.card_data, self.user.get_short_name())