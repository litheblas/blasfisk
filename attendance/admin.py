from django.contrib import admin
from attendance.models import Attendance, Comment
#from blasbase.models import Customer


class AttendanceAdmin(admin.ModelAdmin):
    class Meta:
        model = Attendance

class CommentAdmin(admin.ModelAdmin):
    class Meta:
        model = Comment


# Register your models here.
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Comment, CommentAdmin)