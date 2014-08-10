from django.contrib import admin
from events.models import *
from blasbase.models import Customer

class EventInformationInline(admin.TabularInline):
    model = EventInformation


class EventAdmin(admin.ModelAdmin):
    inlines = [EventInformationInline]
    filter_horizontal = ['visible_to']

# Register your models here.
admin.site.register(Event, EventAdmin)
admin.site.register(EventType)
admin.site.register(Customer)