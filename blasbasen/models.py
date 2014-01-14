# -*- coding: utf-8 -*-
import uuid
import datetime
from django.db import models
from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractBaseUser
from localflavor.se.forms import SEOrganisationNumberField
from litheblas.globals import countries

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
    email = models.EmailField(verbose_name='email address', max_length=256, unique=True, db_index=True)
    username = models.CharField(max_length=256, default=str(uuid.uuid1())) #TODO: Kolla om det går att lösa så detta fält kan tas bort. Finns bara för att Mezzanine inte ska balla ur.
    is_active = models.BooleanField(default=True, help_text="Detta är INTE ett fält för att markera att någon blivit gamling") #Ska inte användas för att markera gamlingsskap osv.! Det görs mycket bättre på automatisk väg via posts
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    #Personal information
    first_name = models.CharField(max_length=256)
    nickname = models.CharField(max_length=256, blank=True)
    last_name = models.CharField(max_length=256)
    date_of_birth = models.DateField(blank=True, null=True)
    personal_id_number = models.CharField(max_length=4, blank=True, help_text="Sista 4 siffrorna i personnumret") #Last 4 characters in Swedish personal id number
    
    posts = models.ManyToManyField('Post', through='Assignment')
    
    #Address information
    address = models.CharField(max_length=256, blank=True)
    postcode = models.CharField(max_length=256, blank=True)
    city = models.CharField(max_length=256, blank=True)
    country = models.CharField(max_length=2, choices=countries, default='SE', blank=True)
    
    
    liu_id = models.CharField(max_length=8, verbose_name='LiU-ID', blank=True)
    
    
    about = models.TextField(blank=True) #Kan förslagsvis användas för att t.ex. beskriva vad som gör en hedersmedlem så hedersvärd eller bara fritext av personen själv.
    special_diets = models.ManyToManyField('SpecialDiet', blank=True, null=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    def is_active_member(self):
        #TODO: Returnera en bool för om användaren har medlemsskap eller något åtagande i föreningen.
        pass
    
    def get_assignments(self, readable=False):
        #Exkludera objekt som avslutats innan detta dygn (detta ser till att objekt utan slutdatum inte utesluts), 
        #filtrera sedan ut de objekt som påbörjats innan detta dygn
        return self.membershipassignment_set.exclude(end_date__lt=datetime.date.today()).filter(start_date__lte=datetime.date.today())

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
    """Exempelvis trumpet, styrelsen, kompet, funktionärer, gamlingar/hedersmedlemmar, kommittéer etc.. Denna datatyp (tillsammans med Post) styr medlemsskap i grupper."""
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']
    
    def get_members(self, current=True):
        #TODO: Slå upp alla poster som finns i sektionen. Vilka människor är knutna till dessa poster? Om current är True hämta endast nuvarande medlemmar
        pass
    
    def __unicode__(self):
        return self.name

class Post(models.Model):
    """Exempelvis elbas, dictator, gamling, hedersmedlem, vän till blåset, sektionschef etc.. 
    Bäst att spara gamling som en egen slags medlemstyp utan sektion eftersom systemet 
    själv kan hålla reda på vilka sektioner man tillhört.
    Avlidna/uteslutna medlemmar tas lämpligtvis bort från alla poster. 
    
    #TODO: Ett skript som körs vid ändring av posterna tilldelar gruppmedlemsskap i Djangos egna tabeller.
    Det är alltså gruppmedlemsskap som styr egentliga rättigheter och inte denna tabell.
    Detta eftersom Django redan har inbyggda rutiner för rättighetshantering
    som fungerar mycket bra och är utbyggbara."""
    
    section = models.ForeignKey('Section', blank=True, null=True)
    post = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    show_in_timeline = models.BooleanField(default=True, help_text="Ska ett medlemskap på denna post visas i tidslinjen? (Tidslinjen som inte finns ännu)")
    
    #TODO: En egenskap för om posten är arkiverad också kanske? Typ generalbas

    
    class Meta:
        unique_together = (('section', 'post',),)
        ordering = ['section', 'post']
    
    def __unicode__(self):
        if self.section:
            return u'{0} / {1}'.format(self.section.name, self.post)
        return self.post

class Assignment(models.Model):
    """Mellantabell som innehåller info om varje användares medlemsskap/uppdrag på olika poster."""
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'medlemsskap/uppdrag'
        verbose_name_plural = verbose_name
    
    #TODO: När instanser av denna sparas skall gruppmedlemsskap uppdateras, både från poster och sektioner. Dessutom behöver någon slags skript köras varje natt för att uppdatera poster som gått ut.
    
    def is_ongoing(self):
        #TODO: Kolla om startdatum finns och om före dagens datum. 
        #Om ja, kolla om slutdatum finns och om efter dagens datum. 
        #Om ja, returnera True.
        pass
        
    
    def __unicode__(self):
        return u'{0}: {1}'.format(self.user.get_short_name(), self.post)

class SpecialDiet(models.Model):
    name = models.CharField(max_length=256,help_text='Anges i formen "Allergisk mot...", "Nykterist" etc.')

    def __unicode__(self):
        return self.name
    
class Customer(models.Model):
    name = models.CharField(max_length=256)
    organisation_number = SEOrganisationNumberField(min_length=0) #TODO: Kolla om det verkligen går att lämna blankt #Accepterar även personnummer
    comments = models.TextField(blank=True)
    
    contact = models.CharField(max_length=256, blank=True) #Kontaktperson
    phone_number = models.CharField(max_length=64, blank=True)
    
    #Address information
    address = models.CharField(max_length=256, blank=True)
    postcode = models.CharField(max_length=256, blank=True)
    city = models.CharField(max_length=256, blank=True)
    country = models.CharField(max_length=2, choices=countries, default='SE', blank=True)
    
    def __unicode__(self):
        return self.name

class Card(models.Model):
    enabled = models.BooleanField(default=True, help_text="Avmarkera om du tillfälligt vill spärra ditt kort")
    card_data = models.CharField(max_length=256, help_text="Be någon kolla i loggen efter ditt kortnummer") #TODO: Kolla exakt vad av kortets data som läses av. Vad av detta skall lagras?
    user = models.ForeignKey(User) #Kort _måste_ associeras med en användare. Låt det vara så så slipper vi "temporära lösningar" och vilsna kort som ingen vet vem de tillhör.
    description = models.CharField(max_length=256, blank=True, help_text="Anges förslagsvis om du har fler än ett kort")
    
    def __unicode__(self):
        return '{0} ({1})'.format(self.card_data, self.user.get_short_name())
