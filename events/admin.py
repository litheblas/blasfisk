from django.contrib import admin
from events.models import *
from blasbase.models import Customer


class EventInformationInline(admin.TabularInline):
    model = EventInformation
    filter_horizontal = ['functions']
    extra = 1


class EventAdmin(admin.ModelAdmin):
    inlines = [EventInformationInline]


# Register your models here.
admin.site.register(Event, EventAdmin)
admin.site.register(EventType)
admin.site.register(Customer)