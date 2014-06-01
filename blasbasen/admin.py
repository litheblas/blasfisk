from django.contrib import admin

from django.contrib.auth.models import Group
from blasbasen.models import Avatar, User, Person, Section, Post, Assignment, SpecialDiet, Card
#from mailing.models import Membership as MailingMembership
#from watcher.models import Watcher

class AssignmentInline(admin.TabularInline):
    model = Assignment
    extra = 1

class AvatarInline(admin.TabularInline):
    model = Avatar
    extra = 1
    
#class MailingListInline(admin.TabularInline):
#    model = MailingMembership

class CardInline(admin.TabularInline):
    model = Card
    extra = 1

class PostInline(admin.TabularInline):
    model = Post
    extra = 1
    
class GroupMemberInline(admin.TabularInline):
    model = User.groups.through
    readonly_fields = ['user']
    extra = 0
    
class UserInline(admin.StackedInline):
    model = User
    max_num = 1
    

#class WatcherInline(admin.TabularInline):
#    model = Watcher

class GroupAdmin(admin.ModelAdmin):
    #inlines = [WatcherInline,GroupMemberInline]
    inlines = [GroupMemberInline]

    exclude = ('groups',)

class SectionAdmin(admin.ModelAdmin):
    inlines = [PostInline]

class PersonAdmin(admin.ModelAdmin):
    #inlines = [AvatarInline, AssignmentInline, CardInline, MailingListInline, UserInline]

    inlines = [AvatarInline, AssignmentInline, CardInline, UserInline]
    
    list_display = ('first_name', 'nickname', 'last_name')
#     fieldsets = (
#         (None, {
#             'fields': (('first_name', 'nickname', 'last_name'), ('date_of_birth', 'personal_id_number'))
#         }),
#         ('Auth and perm', {
#             'fields':()
#         })
#     )

admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Post)
admin.site.register(Section, SectionAdmin)
#admin.site.register(Assignment)
admin.site.register(SpecialDiet)