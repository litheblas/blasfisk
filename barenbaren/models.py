from django.db import models
from litheblas.events.models import Event as BasenEvent

class Event(models.Model):
    basen_event = models.OneToOneField(BasenEvent)
    