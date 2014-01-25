from django.contrib import admin
from django.contrib.auth.models import Group
from litheblas.blasbasen.models import Avatar, User, Person, Section, Post, Assignment, SpecialDiet, Card
from litheblas.mailing.models import Membership as MailingMembership
from litheblas.watcher.models import Watcher

class AssignmentInline(admin.TabularInline):
    model = Assignment

class AvatarInline(admin.TabularInline):
    model = Avatar
    extra = 1
    
class MailingListInline(admin.TabularInline):
    model = MailingMembership

class CardInline(admin.TabularInline):
    model = Card
    extra = 1

class PostInline(admin.TabularInline):
    model = Post
    
class GroupMemberInline(admin.TabularInline):
    model = User.groups.through
    readonly_fields = ['user']
    extra = 0
    
class UserInline(admin.StackedInline):
    model = User
    max_num = 1
    

class WatcherInline(admin.TabularInline):
    model = Watcher

class GroupAdmin(admin.ModelAdmin):
    inlines = [WatcherInline,GroupMemberInline]
    exclude = ('groups',)

class SectionAdmin(admin.ModelAdmin):
    inlines = [PostInline]

class PersonAdmin(admin.ModelAdmin):
    inlines = [AvatarInline, AssignmentInline, CardInline, MailingListInline, UserInline]
    
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
#admin.site.register(Post)
admin.site.register(Section, SectionAdmin)
#admin.site.register(Assignment)
admin.site.register(SpecialDiet)