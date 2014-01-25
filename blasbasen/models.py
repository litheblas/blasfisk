# -*- coding: utf-8 -*-
import uuid
import datetime
from django.db import models
from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractBaseUser
from localflavor.se.forms import SEOrganisationNumberField
from litheblas.globals import countries

class Person(models.Model):
    #Personal information
    first_name = models.CharField(max_length=256, verbose_name='förnamn')
    nickname = models.CharField(max_length=256, blank=True, verbose_name='blåsnamn')
    last_name = models.CharField(max_length=256, verbose_name='efternamn')
    date_of_birth = models.DateField(blank=True, null=True, verbose_name='födelsedatum')
    personal_id_number = models.CharField(max_length=4, blank=True, verbose_name='personnummer', help_text="Sista 4 siffrorna i personnumret") #Last 4 characters in Swedish personal id number
    liu_id = models.CharField(max_length=8, blank=True, verbose_name='LiU-ID')
    
    posts = models.ManyToManyField('Post', through='Assignment', verbose_name='poster')
    
    #Address information
    address = models.CharField(max_length=256, blank=True, verbose_name='adress')
    postcode = models.CharField(max_length=256, blank=True, verbose_name='postnummer')
    city = models.CharField(max_length=256, blank=True, verbose_name='stad')
    country = models.CharField(max_length=2, choices=countries, default='SE', blank=True, verbose_name='land')
    
    about = models.TextField(blank=True, verbose_name='om') #Kan förslagsvis användas för att t.ex. beskriva vad som gör en hedersmedlem så hedersvärd eller bara fritext av personen själv.
    special_diets = models.ManyToManyField('SpecialDiet', blank=True, null=True, verbose_name='speciella kostvanor')
    
    class Meta:
        ordering = ['first_name', 'last_name', 'nickname']
        verbose_name = 'person'
        verbose_name_plural = 'personer'
    
    def get_assignments(self, readable=False):
        #Exkludera objekt som avslutats innan detta dygn (detta ser till att objekt utan slutdatum inte utesluts), 
        #filtrera sedan ut de objekt som påbörjats innan detta dygn
        return self.assignment_set.exclude(end_date__lt=datetime.date.today()).filter(start_date__lte=datetime.date.today())
    
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
    
    full_name = property(get_full_name)
    short_name = property(get_short_name)


class UserManager(BaseUserManager):
    """Plankat från Djangos dokumentation. Används för Blåsbasens användarmodell."""
    def create_user(self, email, password):
        if not email:
            raise ValueError('Users must have an email address')
        
        if not password:
            raise ValueError('Users must have a password')
        
        #TODO: Fixa nåt snyggare
        person = Person(first_name='root', last_name='root')
        person.save()

        user = self.model(
            person=person,
            email=self.normalize_email(email),
            password=password,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        #Use the normal method for creating users
        user = self.create_user(
            email,
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
    email = models.EmailField(max_length=256, unique=True, db_index=True, verbose_name='e-postadress')
    username = models.CharField(max_length=256, default=str(uuid.uuid1()), verbose_name='användar-ID') #TODO: Kolla om det går att lösa så detta fält kan tas bort. Finns bara för att Mezzanine inte ska balla ur.
    is_active = models.BooleanField(default=True, verbose_name='aktivt konto', help_text="Detta är INTE ett fält för att markera att någon blivit gamling") #Ska inte användas för att markera gamlingsskap osv.! Det görs mycket bättre på automatisk väg via posts
    is_admin = models.BooleanField(default=False, verbose_name='administratörskonto (?)', help_text='#TODO: Osäker på vad detta fält faktiskt används för. Kolla upp.')
    is_staff = models.BooleanField(default=False, verbose_name='maktkonto', help_text='Bestämmer om användaren kan logga in i admingränssnittet')
    
    person = models.OneToOneField(Person, related_name='user', verbose_name='person')
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    
    class Meta:
        ordering = ['person', 'email']
        verbose_name = 'användarkonto'
        verbose_name_plural = 'användarkonton'
    
    #Används internt av Django
    def get_full_name(self):
        return self.person.full_name

    #Används internt av Django
    def get_short_name(self):
        return self.person.short_name
        
    def __unicode__(self):
        return self.person.full_name
    
    full_name = property(get_full_name)
    short_name = property(get_short_name)

class Section(models.Model):
    """Exempelvis trumpet, styrelsen, kompet, funktionärer, gamlingar/hedersmedlemmar, kommittéer etc.. Denna datatyp (tillsammans med Post) styr medlemsskap i grupper."""
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    
    
    class Meta:
        ordering = ['name']
        verbose_name = 'sektion'
        verbose_name_plural = 'sektioner'
    
    def get_people(self, current=True):
        people = []
        for post in self.post_set.all():
            people.extend(post.get_people(current))
        return people
    
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
        verbose_name = 'post'
        verbose_name_plural = 'poster'
    
    def get_people(self, current=True):
        people=[]
        if current:
            #Att vi väljer att exkludera åtaganden med slutdatum innan idag ser till att åtaganden utan slutdatum också kommer med.
            assignments = self.assignment_set.exclude(end_date__lt=datetime.date.today()).filter(start_date__lte=datetime.date.today())
        elif not current:
            #Välj ut åtaganden med startdatum tidigare än eller lika med idag.
            assignments = self.assignment_set.filter(start_date__lte=datetime.date.today())
        
        # select_related för att minska antalet databasfrågor en aning.
        for assig in assignments.select_related('person'):
            people.append(assig.person)
        return people
    
    def __unicode__(self):
        if self.section:
            return u'{0} / {1}'.format(self.section.name, self.post)
        return self.post

class Assignment(models.Model):
    """Mellantabell som innehåller info om varje användares medlemsskap/uppdrag på olika poster."""
    person = models.ForeignKey(Person)
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
        return u'{0}: {1}'.format(self.person.get_short_name(), self.post)

class SpecialDiet(models.Model):
    name = models.CharField(max_length=256, verbose_name='beskrivning', help_text='Anges i formen "Allergisk mot...", "Nykterist" etc.')
    
    class Meta:
        ordering = ['name']
        verbose_name = 'speciell kostvana'
        verbose_name_plural = 'speciella kostvanor'

    def __unicode__(self):
        return self.name
    
class Customer(models.Model):
    name = models.CharField(max_length=256, verbose_name='namn')
    organisation_number = SEOrganisationNumberField(min_length=0) #TODO: Fixa verbose_name. Kolla om det verkligen går att lämna blankt #Accepterar även personnummer
    comments = models.TextField(blank=True, verbose_name='kommentar')
    
    contact = models.CharField(max_length=256, blank=True, verbose_name='kontaktperson')
    phone_number = models.CharField(max_length=64, blank=True, verbose_name='telefonnummer')
    
    #Address information
    address = models.CharField(max_length=256, blank=True, verbose_name='adress')
    postcode = models.CharField(max_length=256, blank=True, verbose_name='postnummer')
    city = models.CharField(max_length=256, blank=True, verbose_name='stad')
    country = models.CharField(max_length=2, choices=countries, default='SE', blank=True, verbose_name='land')
    
    class Meta:
        ordering = ['name', 'contact']
        verbose_name = 'kund'
        verbose_name_plural = 'kunder'
    
    def __unicode__(self):
        return self.name

class Card(models.Model):
    enabled = models.BooleanField(default=True, verbose_name='aktiverat', help_text="Avmarkera om du tillfälligt vill spärra ditt kort")
    card_data = models.CharField(max_length=256, verbose_name='kortdata', help_text="Be någon kolla i loggen efter ditt kortnummer") #TODO: Kolla exakt vad av kortets data som läses av. Vad av detta skall lagras?
    person = models.ForeignKey(Person, verbose_name='person') #Kort _måste_ associeras med en person. Låt det vara så så slipper vi "temporära lösningar" och vilsna kort som ingen vet vem de tillhör.
    description = models.CharField(max_length=256, verbose_name='beskrivning', blank=True, help_text="Anges förslagsvis om du har fler än ett kort")
    
    class Meta:
        verbose_name = 'kort'
        verbose_name_plural = 'kort'
    
    def __unicode__(self):
        return u'{0} ({1})'.format(self.card_data, self.person.get_short_name())
