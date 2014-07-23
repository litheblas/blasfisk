# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Card(models.Model):
    enabled = models.BooleanField(default=True, verbose_name=_('enabled'),
                                  help_text=_(u"Avmarkera om du tillfälligt vill spärra ditt kort"))
    person = models.ForeignKey('blasbase.Person', related_name='cards')  # Kort _måste_ associeras med en person. Låt det vara så så slipper vi "temporära lösningar" och vilsna kort som ingen vet vem de tillhör.
    description = models.CharField(max_length=256, blank=True, verbose_name=_('description'),
                                   help_text=_(u"Anges förslagsvis om du har fler än ett kort"))

    class Meta:
        abstract = True

    def __str__(self):
        return u'{0} ({1})'.format(self.card_data, self.person.get_short_name())


class MagnetCard(Card):
    card_data = models.CharField(max_length=256, verbose_name=_('card data'))


class RFIDCard(Card):
    card_data = models.CharField(max_length=512, verbose_name=_('card data'))