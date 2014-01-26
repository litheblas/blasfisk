# -*- coding: utf-8 -*-

from django.contrib import admin
from watcher.models import Watcher

class WatcherAdmin(admin.ModelAdmin):
    list_display = ('description', 'group', 'list')
    
    filter_horizontal = ['sections', 'posts']
    fieldsets = (
        (None, {
            'fields': ('description',)}),
        ('Hämta användare från...', {
            'description': '#TODO: En bra beskrivning här',
            'fields': ('sections', 'posts')}),
        ('Alternativ', {
            'fields': ('current',)}),
        ('Lägg till användare i...', {
            'description': 'Välj i vilken grupp och/eller vilken mailinglista valda sektions-/postmedlemmar ska hamna.',
            'fields': ('group', 'list')})
    )

admin.site.register(Watcher, WatcherAdmin)