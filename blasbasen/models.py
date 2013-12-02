# -*- coding: utf-8 -*-
import uuid
import datetime
from django.db import models
# from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractBaseUser, Group
from localflavor.se.forms import SEOrganisationNumberField

# TODO: Lägg till alla länder
countries = (
    ('SE', 'Sverige'),
    ('US', 'USA')
)

class UserManager(BaseUserManager):
    """Plankat från Djangos dokumentation. Används för Blåsbasens användarmodell."""
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
    username = models.CharField(max_length=255, default=str(uuid.uuid1())) #TODO: Kolla om det går att lösa så detta fält kan tas bort. Finns bara för att Mezzanine inte ska balla ur.
    is_active = models.BooleanField(default=True) #Ska inte användas för att markera gamlingsskap osv.! Det görs mycket bättre på automatisk väg via posts
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
    
    posts = models.ManyToManyField('Post', through='MembershipAssignment') #Föreslår att detta bara tilldelas människor som faktiskt har en formell anknytning till föreningen.
    
    about = models.TextField() #Kan förslagsvis användas för att t.ex. beskriva vad som gör en hedersmedlem så hedersvärd eller bara fritext av personen själv.
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    def is_active_member(self):
        #TODO: Returnera en bool för om användaren har medlemsskap eller något åtagande i föreningen.
        pass
    
    def get_assignments(self, readable=False):
        #Exkludera objekt som avslutats innan detta dygn (detta ser till att objekt utan slutdatum inte utesluts), 
        #filtrera sedan ut de objekt som påbörjats innan detta dygn
        obj = self.membershipassignment_set.exclude(end_date__lt=datetime.date.today()).filter(start_date__lte=datetime.date.today())
        
        #TODO: 
        if readable:
            #Ger en lista med strängar i formatet 'Sektion: post'
            l = []
            for i in obj:
                #TODO: 
                pass
        return obj

    #Används internt av Django
    def get_full_name(self):
        if self.nickname:
            return u'{0} "{1}" {2}'.format(self.first_name, self.nickname, self.last_name) # Leif "Pappa Blås" Holm

        return u'{0} {1}'.format(self.first_name, self.last_name) # Leif Holm

    #Används internt av Django
    def get_short_name(self):
        if self.nickname:
            return self.nickname # Pappa Blås

        return u'{0} {1}'.format(self.first_name, self.last_name[0]) # Leif H

    def __unicode__(self):
        return self.get_full_name()

class Section(models.Model):
    """Exempelvis trumpet, styrelsen, kompet, funktionärer, gamlingar/hedersmedlemmar, kommittéer etc."""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['name']
    
    def get_members(self, current=True):
        #TODO: Slå upp alla poster som finns i sektionen. Vilka människor är knutna till dessa poster? Om current är True hämta endast nuvarande medlemmar
        pass
    
    def __unicode__(self):
        return self.name

class Post(models.Model):
    """Exempelvis elbas, dictator, gamling, hedersmedlem. 
    Bäst att spara gamling som en egen slags medlemstyp eftersom 
    man inte blir gamling på nåt specifikt instrument/sektion. 
    
    Ett skript som körs vid ändring av posterna tilldelar gruppmedlemsskap i Djangos egna tabeller.
    #TODO: Hur ska dessa grupper genereras automatiskt?
    Det är alltså gruppmedlemsskap som styr rättigheter och inte denna tabell.
    Detta eftersom Django redan har inbyggda rutiner för rättighetshantering
    som fungerar mycket bra och är utbyggbara"""
    
    section = models.ForeignKey('Section', blank=True, null=True)
    post = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    #TODO: En egenskap för om posten är arkiverad också kanske? Typ generalbas

    
    class Meta:
        unique_together = (('section', 'post',),)
        ordering = ['section', 'post']
    
    def __unicode__(self):
        if self.section:
            return u'{0} / {1}'.format(self.section.name, self.post)
        return self.post

class MembershipAssignment(models.Model):
    user = models.ForeignKey('User')
    post = models.ForeignKey('Post')
    
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'membership/assignment'
        verbose_name_plural = 'memberships/assignments'
    
    def is_ongoing(self):
        #TODO: Kolla om startdatum finns och om före dagens datum. 
        #Om ja, kolla om slutdatum finns och om efter dagens datum. 
        #Om ja, returnera True.
        pass
        
    
    def __unicode__(self):
        return u'{0}: {1}'.format(self.user.get_short_name(), self.post)
    
class SpecialDiet(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name
    
class Customer(models.Model):
    name = models.CharField(max_length=255)
    organisation_number = SEOrganisationNumberField()
    comments = models.TextField()
    
    contact = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=64)
    
    #Address information
    address = models.CharField(max_length=255, blank=True)
    postcode = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=2, choices=countries, default='SE', blank=True)
    
    def __unicode__(self):
        return self.name

"""
class GroupFilter(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    group = models.ForeignKey(Group)
    user_query = models.TextField() # A Django query that returns the desired users
    
    def __unicode__(self):
        return self.name
"""

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
