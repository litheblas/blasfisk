from django.db import models

class Facility(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    
class Equipment(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()