# -*- coding: utf-8 -*-

from django.contrib import admin

from attendance.models import Attendance, Comment
from datetime import datetime, time

class AttendanceAdmin(admin.ModelAdmin):
    # Design to the admin-page
    list_display = ('get_event_start', 'event', 'person', 'attended', 'penalty', 'comment')
    list_filter = ['attended', 'person', 'event']
    list_per_page = 200
    ordering = ['-event__start']
    search_fields = ['person__first_name', 'person__nickname', 'person__last_name', 'event__start']

    def get_event_start(self, obj):
        return obj.event.start
    get_event_start.short_description = 'Event start'
    get_event_start.admin_order_field = 'event__start'

    class Meta:
        model = Attendance


class CommentAdmin(admin.ModelAdmin):
    class Meta:
        model = Comment


# Register your models here.
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Comment, CommentAdmin)