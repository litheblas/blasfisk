from django.db import models
from litheblas.blasbasen.models import User
from litheblas.events.models import Attendance

#class Event(models.Model):
#    pass

class Balance(models.Model):
    user = models.OneToOneField(User)
    balance = models.DecimalField(max_digits=9, decimal_places=2)
    
    def __unicode__(self):
        return u'{0}: {1}'.format(self.user.get_short_name(), self.balance)

class Consumption(models.Model):
    """Knyter samman användare, evenemang, dag och streck"""
    event_user = models.ForeignKey(Attendance)
    date = models.DateField()
    amount = models.PositiveIntegerField()
    
    class Meta:
        unique_together = [['event_user', 'date'],]
    
    def __unicode__(self):
        return u'{0}: {1}, {2} cl'.format(self.date, self.event_user, self.amount)