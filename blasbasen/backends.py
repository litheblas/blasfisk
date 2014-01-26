# -*- coding: utf-8 -*-
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model

def make_permission_set(source):
    """ Skapar ett set av Permissions i det format Django förväntar sig.
    Fritt efter django.contrib.auth.backends.ModelBackend.get_all_permissions """
    return set(["%s.%s" % (permission.content_type.app_label, permission.codename) for permission in source])

class BlasBackend(ModelBackend):
    """ Blåsbasens auth-backend. Subklassar Djangos egna men byter ut en metod samt lägger till en för att hantera rättigheter från sektioner och poster. 
    Jag har modifierat en del så det kan vara bra att hålla en öga på dessa metoder vid byte av Django-version. //Olle """
    
    def get_assignment_permissions(self, user_obj, obj=None):
        """
        Plankat från django.contrib.auth.backends.ModelBackend.get_group_permissions men anpassat för sektioner/poster
        """
        if user_obj.is_anonymous() or obj is not None:
            return set()
        if not hasattr(user_obj, '_assignment_perm_cache'):
            if user_obj.is_superuser:
                user_obj._assignment_perm_cache = make_permission_set(Permission.objects.all())
            else:
                user_obj._assignment_perm_cache = get_user_model().get_assignment_permissions(user_obj)
        return user_obj._assignment_perm_cache
    
    def get_all_permissions(self, user_obj, obj=None):
        """
        Fritt efter django.contrib.auth.backends.ModelBackend.get_all_permissions men anropar dessutom get_assignment_permissions()
        """
        if user_obj.is_anonymous() or obj is not None:
            return set()
        if not hasattr(user_obj, '_perm_cache'):
            user_obj._perm_cache = make_permission_set(user_obj.user_permissions.select_related()) # Användarrättigheter
            #user_obj._perm_cache = set(["%s.%s" % (p.content_type.app_label, p.codename) for p in user_obj.user_permissions.select_related()]) # Användarrättigheter
            user_obj._perm_cache.update(self.get_group_permissions(user_obj)) # Grupprättigheter
            user_obj._perm_cache.update(self.get_assignment_permissions(user_obj)) # Sektions-/posträttigheter
        return user_obj._perm_cache