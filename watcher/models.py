# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import Group

class Watcher(models.Model):
    """Lägger automatiskt till användare till en grupp och/eller mailinglista baserat på sektion eller post."""
    #Leta i
    sections = models.ManyToManyField('blasbasen.Section', blank=True, null=True, help_text="En sektion som skall övervakas. Alla medlemmar i alla poster i sektionen inkluderas.")
    posts = models.ManyToManyField('blasbasen.Post', blank=True, null=True, help_text="En specifik post som skall övervakas. Om posten ingår i någon sektion som angetts behöver du inte ange den här.")
    current = models.BooleanField(default=True, help_text="Inkludera endast aktiva.")
    
    #Lägg till i
    group = models.ForeignKey(Group, blank=True, null=True)
    list = models.ForeignKey('mailing.MailingList', blank=True, null=True)
    
    #TODO: Överväg att lösa det här på ett sätt som inte skickar så in i hundan många frågor.
    def get_users(self):
        users = []
        for section in self.sections.all():
            users.extend(section.get_users(self.current))
        for post in self.posts.all():
            users.extend(post.get_users(self.current))
        return users
    
    def apply(self):
        #TODO: Allt
        
        users = self.get_users()
        
        #Lägg till personer i grupp
        for user in users:
            self.group.user_set.add(user)
            
            
        
        pass