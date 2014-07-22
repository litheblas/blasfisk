# -*- coding: utf-8 -*-

from django.contrib import admin

from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from blasbase.models import Avatar, User, Person, Section, Post, Assignment, SpecialDiet, Card
from blasbase.forms import BlasUserChangeForm, BlasUserCreationForm
#from mailing.models import Membership as MailingMembership
#from watcher.models import Watcher
from django.utils.translation import ugettext_lazy as _

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
    extra = 0

class BlasUserInline(admin.StackedInline):
    
    form = BlasUserChangeForm

class BlasUserAdmin(admin.StackedInline, UserAdmin):
    # TODO: Bättre
    model = User
    fk_name = 'person'
    max_num = 1
    extra = 0

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        #(_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')}
        ),
    )
    form = BlasUserChangeForm
    add_form = BlasUserCreationForm
    #list_display = ('username', 'is_staff')
    #search_fields = ('username',)
    #ordering = ('username',)
    
    def __init__(self, parent_model, admin_site):
        self.admin_site = admin_site
        self.parent_model = parent_model
        self.opts = self.model._meta
        
        if self.verbose_name is None:
            self.verbose_name = self.model._meta.verbose_name
        if self.verbose_name_plural is None:
            self.verbose_name_plural = self.model._meta.verbose_name_plural

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

    inlines = [AvatarInline, AssignmentInline, CardInline, BlasUserAdmin]
    
    list_display = ('first_name', 'nickname', 'last_name')
#     fieldsets = (
#         (None, {
#             'fields': (('first_name', 'nickname', 'last_name'), ('date_of_birth', 'personal_id_number'))
#         }),
#         ('Auth and perm', {
#             'fields':()
#         })
#     )



#admin.site.register(User, BlasUserAdmin)

admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Post)
admin.site.register(Section, SectionAdmin)
#admin.site.register(Assignment)
admin.site.register(SpecialDiet)