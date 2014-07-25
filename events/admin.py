from django.contrib import admin
from events.models import Event, EventType
from blasbase.models import Customer

# Register your models here.
admin.site.register(Event)
admin.site.register(EventType)
admin.site.register(Customer)