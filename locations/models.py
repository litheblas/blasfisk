from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from globals import COUNTRIES


# Create your models here.


class AddressMixin(models.Model):
    address = models.CharField(max_length=256, blank=True, verbose_name=_('address'))
    post_code = models.CharField(max_length=256, blank=True, verbose_name=_('post code'))  # Byt namn till post_code
    city = models.CharField(max_length=256, blank=True, verbose_name=_('city'))
    country = models.CharField(max_length=2, choices=COUNTRIES, default='SE', blank=True, verbose_name=_('country'))

    class Meta:
        abstract = True


@python_2_unicode_compatible
class Location(AddressMixin, models.Model):
    name = models.CharField(max_length=256, blank=True, verbose_name=_('name'))
    _display_name = models.CharField(max_length=256, blank=True, verbose_name=_('display name'), help_text=_('Used for displaying a different name in public.'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    latitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True, verbose_name=_('latitude'))
    longitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True, verbose_name=_('longitude'))

    def __str__(self):
        return self.name

    @property
    def display_name(self):
        return self._display_name or self.name

    @property
    def google_maps_url(self):
        if self.latitude and self.longitude:
            return 'https://maps.google.com/?q={0},{1}'.format(self.latitude, self.longitude)
        else:
            return None