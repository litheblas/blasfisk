from django.contrib import admin
from litheblas.blasbasen.models import User, Section, Post, Assignment, SpecialDiet, Card
from litheblas.mailing.models import Membership as MailingMembership

class AssignmentInline(admin.TabularInline):
    model = Assignment
    
class MailingListInline(admin.TabularInline):
    model = MailingMembership

class CardInline(admin.TabularInline):
    model = Card
    extra = 1
    
class UserAdmin(admin.ModelAdmin):
    inlines = [AssignmentInline, CardInline, MailingListInline]
    
#     fieldsets = (
#         (None, {
#             'fields': (('first_name', 'nickname', 'last_name'), ('date_of_birth', 'personal_id_number'))
#         }),
#         ('Auth and perm', {
#             'fields':()
#         })
#     )

admin.site.register(User, UserAdmin)
admin.site.register(Post)
admin.site.register(Section)
#admin.site.register(Assignment)
admin.site.register(SpecialDiet)