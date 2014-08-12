# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from events.models import Event
from blasbase.models import Person

# Create your models here.
@python_2_unicode_compatible
class Comment(models.Model):
    text = models.CharField(max_length = 255)

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')

    def __str__(self):
        return self.text


@python_2_unicode_compatible
class Attendance(models.Model):
    event = models.ForeignKey(Event, related_name='events')
    person = models.ForeignKey(Person, related_name='persons')
    comment = models.ForeignKey(Comment, null=True, blank=True, verbose_name=_('comment'))
    attended = models.NullBooleanField()
    penalty = models.BooleanField(default=False)
    
    def __str__(self):
        return u'{0}: {1}'.format(self.event.name, self.person.first_name)