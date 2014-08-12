from django.contrib import admin
from attendance.models import Attendance, Comment


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('get_event_start', 'event', 'person', 'attended', 'penalty', 'comment')
    list_filter = ['person', 'event']

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