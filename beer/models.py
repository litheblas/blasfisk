from django.db import models
from litheblas.blasbasen.models import User

class Balance(models.Model):
    user = models.OneToOneField(User)
    credits = models.IntegerField()
    
    def __unicode__(self):
        return u'{0}: {1}'.format(self.user.get_short_name(), self.credits)

class Consumption(models.Model):
    """Lagrar förbrukning av klipp, för statistikens skull"""
    user = models.ForeignKey(User)
    amount = models.IntegerField()
    when = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return u'{0}: {1}, {2}x'.format(self.when, self.user.get_short_name(), self.amount)