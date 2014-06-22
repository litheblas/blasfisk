# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
import datetime
from django.utils import timezone

from django.core.exceptions import ValidationError

def datetime_before_datetime(start, end, message):
    """Kontrollerar huruvida datum 1 ligger före eller på samma datum/tid som datum 2.
    Reser ValidationError om falskt, annars ingenting. Validerar endast om båda datumen angetts."""
    
    if start and end and start > end:
        raise ValidationError(message)

def date_before_today(date):
    if date:
        datetime_before_datetime(date, datetime.date.today(), _(u'Must not be in the future.'))

def datetime_before_now(datetime):
    if datetime:
        datetime_before_datetime(datetime, timezone.now(), _(u'Must not be in the future.'))