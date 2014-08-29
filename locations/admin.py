from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from locations.models import Location


class LocationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name', '_display_name']}),
        (_('Description'),   {'fields': ['description'],
                              'classes': ['collapse']}),
        (_('Address'),       {'fields': ['address',
                                         'post_code',
                                         'city',
                                         'country']}),
        (_('Coordinates'), {'fields': ['latitude',
                                       'longitude'],
                            'classes': ['collapse']})
    ]

    list_display = ('name', 'address', 'city')
    list_filter = ['city']
    search_fields = ['name', 'address']

# Register your models here.
admin.site.register(Location, LocationAdmin)