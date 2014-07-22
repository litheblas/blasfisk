# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import Group

class Watcher(models.Model):
    """Lägger automatiskt till användare till en grupp och/eller mailinglista baserat på sektion eller post."""
    description = models.CharField(max_length=256, unique=True, help_text='Använd det här fältet för att kortfattat beskriva vilka som inkluderas av filtret. Ex.: "Aktiva trumpetare"')
    
    #Leta i
    sections = models.ManyToManyField('blasbase.Section', blank=True, null=True, verbose_name='sektioner', help_text=u"En sektion som skall övervakas. Alla medlemmar i alla poster i sektionen inkluderas.")
    posts = models.ManyToManyField('blasbase.Post', blank=True, null=True, verbose_name='poster', help_text=u"En specifik post som skall övervakas. Om posten ingår i någon sektion som angetts behöver (och skall) du inte ange den här.")
    current = models.BooleanField(default=True, verbose_name='endast aktiva', help_text=u"Inkludera endast aktiva.")
    
    #Lägg till i
    group = models.ForeignKey(Group, blank=True, null=True, verbose_name='grupp')
    list = models.ForeignKey('mailing.MailingList', blank=True, null=True, verbose_name='mailinglista')
    
    class Meta:
        ordering = ['description']
        verbose_name = 'bevakning'
        verbose_name_plural = 'bevakningar'
    
    def __unicode__(self):
        return self.description
    
    #TODO: Överväg att lösa det här på ett sätt som inte skickar så in i hundan många frågor.
    def get_people(self):
        people = []
        for section in self.sections.all():
            people.extend(section.get_people(self.current))
        for post in self.posts.all():
            people.extend(post.get_people(self.current))
        return people
    
    def apply(self):
        #TODO: Allt
        
        people = self.get_people()
        
        #Lägg till personer i grupp
        for person in people:
            self.group.user_set.add(person.user)