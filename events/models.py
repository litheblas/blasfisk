# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group
from django.db.models.query import QuerySet
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from datetime import datetime
from cms.models.pluginmodel import CMSPlugin

from blasbase.models import PhoneNumber, EmailAddress

ANSWERS = (
    ('yes', _('Yes')),
    ('maybe', _('Maybe')),
    ('no', _('No')),
)


def default_event_type():
    return EventType.objects.get_or_create(name=settings.DEFAULT_EVENT_TYPE)[0].pk


@python_2_unicode_compatible
class EventType(models.Model):
    name = models.CharField(max_length=256, verbose_name=_('name'))

    class Meta:
        verbose_name = _('event type')
        verbose_name_plural = _('event types')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Attendance(models.Model):
    #Skapas när användaren bjuds in till eller själv går med i ett evenemang
    event = models.ForeignKey('Event', verbose_name=_('event'))
    person = models.ForeignKey('blasbase.Person', verbose_name=_('person'))
    
    answer = models.CharField(max_length=8, choices=ANSWERS, blank=True, verbose_name=_('answer'))  # Blank = no answer

    class Meta:
        verbose_name = _('attendance')
        verbose_name_plural = _('attendances')

    def __str__(self):
        return '{0}: {1}'.format(self.event, self.person)


class Contact(models.Model):
    event = models.ForeignKey('Event', verbose_name=_('event'))
    customer = models.ForeignKey('blasbase.Customer', verbose_name=_('customer'))
    department = models.CharField(max_length=256, blank=True, verbose_name=_('department'))
    contact = models.CharField(max_length=256, blank=True, verbose_name=_('contact person'))
    comments = models.TextField(blank=True, verbose_name=_('comments'))
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=_('price'))

    class Meta:
        verbose_name = _('contact')
        verbose_name_plural = _('contacts')


class ContactPhoneNumber(PhoneNumber):
    contact = models.ForeignKey('Contact', related_name='phone_numbers', verbose_name=_('contact'))

    class Meta:
        verbose_name = _('contact phone number')
        verbose_name_plural = _('contact phone numbers')


class ContactEmailAddress(EmailAddress):
    contact = models.ForeignKey('Contact', related_name='email_addresses', verbose_name=_('contact'))

    class Meta:
        verbose_name = _('contact email address')
        verbose_name_plural = _('contact email addresses')


# Funktioner för att filtrera events
class EventQuerySetMixin(object):
    # Kommande event
    def future(self):
        return self.filter(start__gte=datetime.now()).order_by('start')

    # Tidigare event
    def past(self):
        return self.filter(end__lte=datetime.now()).order_by('end')

    # Enbart publika event. För att visa på publika sidan utan inloggning.
    def public(self):
        return self.filter(information__functions__isnull=True)


# Magi som används för att kunna anropa flera av sina egna funktioner på varandra
class EventQuerySet(QuerySet, EventQuerySetMixin):
    pass


class EventManager(models.Manager, EventQuerySetMixin):
    def get_queryset(self):
        return EventQuerySet(model=self.model, using=self._db)


@python_2_unicode_compatible
class Event(models.Model):
    name = models.CharField(max_length=256, verbose_name=_('name'))
    start = models.DateTimeField(verbose_name=_('start'))
    end = models.DateTimeField(null=True, blank=True, verbose_name=_('end'))
    deadline = models.DateTimeField(null=True, blank=True, verbose_name=_('deadline'))
    location = models.ForeignKey('locations.Location', related_name='events', null=True, blank=True,
                                 verbose_name=_('location'))
    event_type = models.ForeignKey('EventType', related_name='events', default=default_event_type,
                                   verbose_name=_('type'))
    attendees = models.ManyToManyField('blasbase.Person', through=Attendance, related_name='events',
                                       blank=True, null=True, verbose_name=_('attendees'))

    cancelled = models.BooleanField(default=False, verbose_name=_('cancelled'))

    customer = models.ManyToManyField('blasbase.Customer', through=Contact, verbose_name=_('customer'))

    objects = EventManager()

    class Meta:
        ordering = ['start']
        verbose_name = _('event')
        verbose_name_plural = _('events')

    def __str__(self):
        return self.name


class EventInformationQuerySetMixin(object):
    def public(self):
        return self.filter(functions__isnull=True)


class EventInformationQuerySet(QuerySet, EventInformationQuerySetMixin):
    pass


class EventInformationManager(models.Manager, EventInformationQuerySetMixin):
    def get_queryset(self):
        return EventInformationQuerySet(model=self.model, using=self._db)


@python_2_unicode_compatible
class EventInformation(models.Model):
    event = models.ForeignKey('Event', related_name='information', verbose_name=_('event'))
    functions = models.ManyToManyField('blasbase.Function', related_name='event_information', blank=True, null=True,
                                       verbose_name=_('functions'))
    content = models.TextField(verbose_name=_('content'))

    objects = EventInformationManager()

    class Meta:
        verbose_name = _('event information')
        verbose_name_plural = _('event information')

    def __str__(self):
        return self.content


class EventViewer(CMSPlugin):
    count = models.PositiveIntegerField(blank=True, null=True)
    event_types = models.ManyToManyField('EventType', blank=True, null=True)

    def copy_relations(self, instance):
        self.event_types = instance.event_types.all()