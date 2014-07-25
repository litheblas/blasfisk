# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Account(models.Model):
    person = models.ForeignKey('blasbase.Person', blank=True, null=True, verbose_name=_('person'))


class TransactionQuerySetMixin(object):
    def balance(self):
        return self.aggregate(models.Sum('amount'))


class TransactionQuerySet(QuerySet, TransactionQuerySetMixin):
    pass


class TransactionManager(models.Manager, TransactionQuerySetMixin):
    def get_queryset(self):
        return TransactionQuerySet(self.model, using=self._db)

@python_2_unicode_compatible
class Transaction(models.Model):
    account = models.ForeignKey(Account, verbose_name=_('account'))
    amount = models.DecimalField(max_digits=9, decimal_places=2, verbose_name=_('amount (kr)'))

    objects = TransactionManager()

    def __str__(self):
        return u'{0}: {1}'.format(self.person.short_name, self.amount)



@python_2_unicode_compatible
class Consumption(models.Model):
    """Knyter samman användare, evenemang, dag och streck"""
    event = models.ForeignKey('events.Event', null=True, blank=True, verbose_name=_('event'))
    person = models.ForeignKey('blasbase.Person', verbose_name=_('person'))
    date = models.DateField(verbose_name=_('date'))
    amount = models.PositiveIntegerField(verbose_name=_('amount (cl)'))
    
    class Meta:
        unique_together = [['event_person', 'date'], ]
    
    def __str__(self):
        return u'{0}: {1}, {2} cl'.format(self.date, self.person.short_name, self.amount)