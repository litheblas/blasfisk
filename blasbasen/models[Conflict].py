# -*- coding: utf-8 -*-
import uuid
from django.db import models
# from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractBaseUser

# TODO: Lägg till alla länder
countries = (
    ('SE', 'Sverige'),
    ('US', 'USA')
)

class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password):
        if not email:
            raise ValueError('Users must have an email address')
        
        if not first_name:
            raise ValueError('Users must have a first name')
        
        if not last_name:
            raise ValueError('Users must have a last name')
        
        if not password:
            raise ValueError('Users must have a password')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            password=password,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        #Use the normal method for creating users
        user = self.create_user(email,
            first_name,
            last_name,
            password,
        )
        
        #Add superuser properties
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    #Auth related information and other fields required by Django
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True, db_index=True)
    username = models.CharField(max_length=255, default=str(uuid.uuid1())) #Temporary field. Needed for not breaking Mezzanine
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    #Personal information
    first_name = models.CharField(max_length=255) #Required
    nickname = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255) #Required
    date_of_birth = models.DateField(blank=True, null=True)
    personal_id_number = models.CharField(max_length=4, blank=True) #Last 4 characters in Swedish personal id number
    
    #Address information
    address = models.CharField(max_length=255, blank=True)
    postcode = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=2, choices=countries, default='SE', blank=True)
    
    
    special_diets = models.ManyToManyField('SpecialDiet', blank=True)
    liu_id = models.CharField(max_length=8, verbose_name='LiU-ID', blank=True)
    card_data = models.CharField(max_length=255, unique=True, blank=True) #Number or other data used to identify user from magnet card
    
    posts = models.ManyToManyField('Post', through='MembershipAssignment')
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    

    def get_full_name(self):
        if self.nickname:
            return u'{0} "{1}" {2}'.format(self.first_name, self.nickname, self.last_name)

        return u'{0} {1}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        if self.nickname:
            return self.nickname

        return u'{0} {1}'.format(self.first_name, self.last_name[0])

    # On Python 3: def __str__(self):
    def __unicode__(self):
        return self.get_full_name()

class Section(models.Model):
    """Exempelvis trumpet, styrelsen, kompet etc."""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.name

class Post(models.Model):
    """Exempelvis elbas, dictator, gamling, hedersmedlem """
    section = models.ForeignKey('Section', blank=True, null=True)
    post = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    def __unicode__(self):
        if self.section:
            return '{0} / {1}'.format(self.section.name, self.post)
        return self.post

class MembershipAssignment(models.Model):
    user = models.ForeignKey('User')
    post = models.ForeignKey('Post')
    
    start_date = models.DateField()
    end_date = models.DateField()
    
    class Meta:
        verbose_name = 'membership/assignment'
        verbose_name_plural = 'memberships/assignments'
    
    def __unicode__(self):
        return '{0}: {1}'.format(self.user.get_short_name(), self.post)
    
class SpecialDiet(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

"""
class User(models.Model):
    user = models.OneToOneField(DjangoUser)
    
    #Blåsnamn
    nickname = models.CharField(max_length=256, blank=True)
    
    #LiU-ID
    liu_id = models.CharField(max_length=8, verbose_name='LiU-ID', blank=True)
    
    birth_date = models.DateField(blank=True, null=True)
    
    #Personnumrets fyra sista siffror
    personal_id_number = models.CharField(max_length=4, blank=True)
    
    #Fält relaterade till adress
    address = models.CharField(max_length=256, blank=True)
    postcode = models.CharField(max_length=256, blank=True)
    city = models.CharField(max_length=256, blank=True)
    country = models.CharField(max_length=2, choices=countries, default='SE', blank=True)

    #Allergier etc.
    special_diets = models.ManyToManyField(SpecialDiet, blank=True)

    def __unicode__(self):
        return self.user.name
        """
