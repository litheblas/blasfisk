# -*- coding: utf-8 -*-
from django.db import models

class MailingList(models.Model):
    name = models.CharField(max_length=256)
    address = models.CharField(max_length=256)
    description = models.TextField(max_length=256, blank=True)
    closed = models.BooleanField(default=False)
    admins = models.ManyToManyField('blasbasen.Person', null=True, blank=True, related_name="mailinglist_admin_set")
    members = models.ManyToManyField('blasbasen.Person', through='Membership', null=True, blank=True, related_name="mailinglist_member_set") # Varför inte grupp? För att alla användare var och en ska kunna välja bort listor man inte vill vara med i även om någon admin/något skript tycker att de borde vara med.
        
    def __unicode__(self):
        return '{0} – {1}'.format(self.address, self.name)

class Membership(models.Model):
    list = models.ForeignKey(MailingList)
    person = models.ForeignKey('blasbasen.Person')
    
    auto = models.BooleanField(default=False) # Anger om medlemskapet är automatiskt tillagt. Ser till att man inte tas ur listor man gått med i manuellt.
    enabled = models.BooleanField(default=True) # Anger om medlemskapet skall inaktiveras. Möjliggör att man kan gå ur listor man hamnat i automatiskt.