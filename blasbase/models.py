# -*- coding: utf-8 -*-
import datetime
from dateutil.relativedelta import relativedelta

from mptt.models import MPTTModel, TreeForeignKey, TreeManager
from django.db import models
from django.db.models.query import QuerySet
from django.db.models import Q
from django.contrib.auth.models import (
    BaseUserManager,
    PermissionsMixin,
    AbstractBaseUser,
    Permission
)
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from imagekit.models import ProcessedImageField

from globals import GENDERS, COUNTRIES, CONTACT_TYPES, generate_filename
from blasbase.backends import make_permission_set
from blasbase import validators
from locations.models import AddressMixin


def generate_avatar_filename(instance, filename):
    return generate_filename(instance, filename, 'avatars')


class PhoneNumber(models.Model):
    type = models.CharField(max_length=16, choices=CONTACT_TYPES, default='private', verbose_name=_('type'))
    country = models.CharField(max_length=2, choices=COUNTRIES, default='SE', blank=True, verbose_name=_('country'))
    phone_number = models.CharField(max_length=64, verbose_name=_('phone number'))

    class Meta:
        abstract = True


class EmailAddress(models.Model):
    type = models.CharField(max_length=16, choices=CONTACT_TYPES, default='private', verbose_name=_('type'))
    email_address = models.CharField(max_length=256, verbose_name=_('email address'))

    class Meta:
        abstract = True


class PersonAddress(AddressMixin):
    type = models.CharField(max_length=16, choices=CONTACT_TYPES, default='private', verbose_name=_('type'))
    person = models.ForeignKey('blasbase.Person', related_name='addresses', verbose_name=_('person'))


class PersonEmailAddress(EmailAddress):
    person = models.ForeignKey('blasbase.Person', related_name='email_addresses', verbose_name=_('person'))


class PersonPhoneNumber(PhoneNumber):
    person = models.ForeignKey('blasbase.Person', related_name='phone_numbers', verbose_name=_('person'))


class PersonQuerySetMixin(object):
    def members(self):
        return self.filter(assignments__in=Assignment.objects.memberships()).distinct()

    def active(self):
        """Hämtar personer som är relaterade till aktiva assignments. distinct() tar bort eventuella dubletter."""
        return self.filter(assignments__in=Assignment.objects.active()).distinct()

    def oldies(self):
        """Hämtar personer som är relaterade till utgångna assignments (för att hitta personerna som _varit_ medlemmar)
        och exkluderar sedan personer som har relationer till aktiva dito. distinct() tar bort eventuella dubletter."""
        return self.filter(assignments__in=Assignment.objects.oldies()).exclude(
            assignments__in=Assignment.objects.active()).distinct()

    def others(self):
        return self.exclude(assignments__in=Assignment.objects.memberships()).distinct()


class PersonQuerySet(QuerySet, PersonQuerySetMixin):
    pass


class PersonManager(models.Manager, PersonQuerySetMixin):
    # TODO: Remove when changing to Django 1.7
    def get_queryset(self):
        return PersonQuerySet(model=self.model, using=self._db)


@python_2_unicode_compatible
class Person(models.Model):
    """Lagrar personer (som i människor) och är den datatyp som nästan allt i Blåsbasen kopplas till."""
    first_name = models.CharField(max_length=256, verbose_name=_('first name'))
    nickname = models.CharField(max_length=256, blank=True, verbose_name=_('nickname'))
    last_name = models.CharField(max_length=256, verbose_name=_('last name'),
                                 help_text=u'Ange gärna tidigare efternamn inom parentes, t.ex. Vidner (Eriksson)')
    gender = models.CharField(max_length=1, choices=GENDERS, blank=True, verbose_name=_('gender'))
    born = models.DateField(blank=True, null=True, verbose_name=_('born'),
                            validators=[validators.date_before_today])
    deceased = models.DateField(blank=True, null=True, verbose_name=_('deceased'),
                                validators=[validators.date_before_today])
    personal_id_number = models.CharField(max_length=4, blank=True, verbose_name=_('personal identification number'),
                                          help_text=u'Sista 4 siffrorna i personnumret')  # Last 4 characters in Swedish personal id number
    liu_id = models.CharField(max_length=8, blank=True, verbose_name=_('LiU-ID'))

    about = models.TextField(blank=True, verbose_name=_('about'))

    special_diets = models.ManyToManyField('SpecialDiet', related_name='people', blank=True, null=True, verbose_name=_('special diets'))
    special_diets_extra = models.CharField(max_length=256, blank=True, verbose_name=_('special diets comments'))

    functions = models.ManyToManyField('Function', through='Assignment', verbose_name=_('functions'))

    last_updated = models.DateTimeField(auto_now=True, verbose_name=_('last updated'))
    old_database_id = models.IntegerField(null=True)
    objects = PersonManager()

    class Meta:
        ordering = ['first_name', 'last_name', 'nickname']
        verbose_name = _('person')
        verbose_name_plural = _('people')

    def __str__(self):
        return self.get_full_name()

    def clean(self):
        cleaned_data = super(Person, self).clean()

        # Validera endast om både födelse- och dödsdatum angetts.
        if self.born and self.deceased:
            validators.datetime_before_datetime(self.born, self.deceased, _(u'Decease date must be after birth date.'))
        return cleaned_data

    def get_age(self):
        if self.born and not self.deceased:
            return relativedelta(datetime.date.today(), self.born)
        elif self.born and self.deceased:
            return relativedelta(self.deceased, self.born)
        return None

    @property
    def memberships(self):
        return self.assignments.memberships()

    @property
    def engagements(self):
        return self.assignments.engagements()

    def get_primary_avatar(self):
        return self.avatars.get(primary=True)

    def get_secondary_avatars(self):
        return self.avatars.exclude(primary=True)

    # Används internt av Django
    def get_full_name(self):
        if self.nickname:
            return u'{0} "{1}" {2}'.format(self.first_name, self.nickname, self.last_name)  # Leif "Pappa Blås" Holm

        return u'{0} {1}'.format(self.first_name, self.last_name)  # Leif Holm

    # Används internt av Django
    def get_short_name(self):
        if self.nickname:
            return self.nickname  # Pappa Blås

        return u'{0} {1}'.format(self.first_name, self.last_name[0])  # Leif H

    @property
    def start_date(self):
        """Hämtar alla assignments som innebär medlemsskap och som inte är provmedlemsskap,
        sorterar stigande på startdatum, tar det första objektet och ger detta objekts startdatum"""
        try:
            return self.assignments.memberships().first().start_date
        except AttributeError:
            # Om man inte har något assignment som passar i filtret alls måste vi hantera det felet på något vis. Då
            # returnerar vi None istället.
            return None

    @property
    def end_date(self):
        a = self.assignments.memberships().order_by('end_date')

        # Om man inte har några sådana assignments eller om någon är pågående returnerar vi None
        if not a or a.filter(pk__in=Assignment.objects.active()):
            return None

        # Annars tar vi det sista objektet och ger dess slutdatum
        return a.last().end_date

    age = property(get_age)
    full_name = property(get_full_name)
    short_name = property(get_short_name)
    primary_avatar = property(get_primary_avatar)
    secondary_avatars = property(get_secondary_avatars)


@python_2_unicode_compatible
class Avatar(models.Model):
    picture = ProcessedImageField(upload_to=generate_avatar_filename, verbose_name=_('picture'))
    person = models.ForeignKey('Person', related_name='avatars', verbose_name=_('person'))
    primary = models.BooleanField(default=True, verbose_name=_('primary'))

    class Meta:
        ordering = ['primary', 'id']

    def __str__(self):
        return u'{0}: {1}'.format(self.person.short_name, self.id)

    def save(self, *args, **kwargs):
        # Sparar objektet som vanligt
        super(Avatar, self).save(*args, **kwargs)

        # Hämtar alla avatarer tillhörande samma person som aktuellt objekt
        avatars = self.person.avatar_set

        if self.primary:
            # Tar bort primary från alla avatarer tillhörande samma människa. Exkluderar aktuellt objekt om det redan finns.
            avatars.exclude(pk=self.pk).update(primary=False)

        else:
            # Om det inte finns någon avatar tillhörande denna person som är märkt som primär...
            if not avatars.filter(primary=True).exists():
                # ...välj den senast tillagda avataren och välj som primär, välj bort aktuellt objekt om det finns
                a = avatars.exclude(pk=self.pk).order_by('-pk')[0]
                a.primary = True
                a.save()

    def get_url(self):
        """Hämtar (publik) URL till bilden"""
        return self.picture.url

    def get_path(self):
        """Hämtar sökväg (i filsystemet) till bilden"""
        return self.picture._get_path()

    url = property(get_url)
    path = property(get_path)


class UserManager(BaseUserManager):
    """Plankat från Djangos dokumentation. Används för Blåsbasens användarmodell."""

    def create_user(self, username, password):
        if not username:
            raise ValueError(u'Users must have a username')

        if not password:
            raise ValueError(u'Users must have a password')

        # TODO: Fixa nåt snyggare
        person = Person(first_name=u'Niklas', last_name=u'Namnlös')
        person.save()

        user = self.model(
            person=person,
            username=username,
            password=password,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        # Use the normal method for creating users
        user = self.create_user(
            username,
            password
        )

        # Add superuser properties
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user


@python_2_unicode_compatible
class User(AbstractBaseUser, PermissionsMixin):
    """
    En avskalad användarmodell vars enda uppgift i stort sett är att lagra användarnamn och lösenord. Resten lagras i
    datatypen Person.
    """
    username = models.CharField(max_length=256, unique=True, db_index=True, verbose_name=_('username'))
    is_active = models.BooleanField(default=True, verbose_name=_('is active'),
                                    help_text=u"Detta är INTE ett fält för att markera att någon blivit gamling")
    is_staff = models.BooleanField(default=False, verbose_name=_('is staff'),
                                   help_text=u'Bestämmer om användaren kan logga in i admingränssnittet')

    person = models.OneToOneField(Person, related_name='user', verbose_name=_('person'))

    objects = UserManager()

    USERNAME_FIELD = 'username'

    class Meta:
        ordering = ['person', 'username']

    def __str__(self):
        return self.get_full_name()

    def get_assignment_permissions(self, obj=None):
        """Hämtar rättigheter från den kopplade personens poster och sektioner"""
        perms = set()
        # set(["%s.%s" % (p.content_type.app_label, p.codename) for p in user_obj.user_permissions.select_related()])
        for assignment in self.person.get_assignments():
            perms.update(assignment.function.get_all_permissions())
        return perms

    # Ersätter Djangos egna get_all_permissions för att få med rättigheter från poster/sektioner 
    def get_all_permissions(self, obj=None):
        perms = super(User, self).get_all_permissions(obj)  # Hämtar rättigheter på vedertaget vis
        perms.update(self.get_assignment_permissions(obj))
        return perms

    @property
    def first_name(self):
        return self.person.first_name

    @property
    def last_name(self):
        return self.person.last_name

    def get_full_name(self):
        return self.person.full_name

    def get_short_name(self):
        return self.person.short_name

    @property
    def email(self):
        return self.person.email

    # Langar lite egenskaper som många appar förväntar sig finnas i User-modellen.
    full_name = property(get_full_name)
    short_name = property(get_short_name)
    #email = property(get_email)


class FunctionManagerMixin(TreeManager):
    def descendants(self, include_self=False):
        return self.all().get_queryset_descendants(self, include_self=include_self).distinct()

    def ancestors(self, include_self=False):
        # http://stackoverflow.com/q/6471354

        #if isinstance(self, EmptyQuerySet):
        #    return self
        queryset = self.none()
        for obj in self.all():
            queryset = queryset | obj.get_ancestors(include_self=include_self)

        return queryset.distinct()

    def people(self):
        """
        Returns people from self and all descendants.
        """
        return Person.objects.filter(functions=self.descendants(include_self=True)).distinct()

    def permissions(self):
        """
        Returns permissions from self and all ancestors.
        """
        return Permission.objects.filter(functions=self.ancestors(include_self=True)).distinct()


class FunctionQuerySet(QuerySet, FunctionManagerMixin):
    pass


class FunctionManager(FunctionManagerMixin):
    def get_queryset(self):
        return FunctionQuerySet(model=self.model, using=self._db).order_by(self.tree_id_attr, self.left_attr)


@python_2_unicode_compatible
class Function(MPTTModel):
    name = models.CharField(max_length=256, verbose_name=_('name'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', verbose_name=_('parent'))

    permissions = models.ManyToManyField(Permission, related_name='functions', null=True, blank=True, verbose_name=_('permissions'))

    membership = models.BooleanField(default=False, verbose_name=_('membership'))
    engagement = models.BooleanField(default=False, verbose_name=_('engagement'))

    _default_manager = FunctionManager()

    class Meta:
        unique_together = ('parent', 'name')

    class MPTTMeta:
        order_insertion_by = ('name',)

    def __str__(self):
        return u'{0}'.format(self.name)

    def people(self):
        return self.get_descendants(include_self=True).people()

    def get_permissions(self):
        return self.get_ancestors(include_self=True).permissions()


class AssignmentQuerySetMixin(object):
    #use_for_related_fields = True

    def defined(self):
        """
        Returns assignments with at least start or end date.
        """
        return self.exclude(start__isnull=True, end__isnull=True)

    def ongoing(self, date=datetime.date.today()):
        """
        Returns defined assignments with...

        Start date undefined or before date
        AND
        End date undefined or after date

        :param date: datetime.date object, default today
        """
        return self.defined().filter(
            Q(start__isnull=True) | Q(start__lte=date),
            Q(end__isnull=True) | Q(end__gte=date)
        )

    def ended(self, date=datetime.date.today()):
        return self.defined().filter(
            Q(end__lt=date)
        )

    def memberships(self, all=False):
        qs = self.filter(function__membership=True).order_by('start')
        if not all:
            qs = qs.exclude(trial=True)
        return qs

    def engagements(self, all=False):
        qs = self.filter(function__engagement=True).order_by('start')
        if not all:
            qs = qs.exclude(trial=True)
        return qs

    def active(self):
        return self.memberships().ongoing()

    def oldies(self):
        return self.memberships().ended()


class AssignmentQuerySet(QuerySet, AssignmentQuerySetMixin):
    pass


class AssignmentManager(models.Manager, AssignmentQuerySetMixin):
    def get_queryset(self):
        return AssignmentQuerySet(model=self.model, using=self._db)


@python_2_unicode_compatible
class Assignment(models.Model):
    """Mellantabell som innehåller info om varje användares medlemsskap/uppdrag på olika poster."""
    person = models.ForeignKey(Person, related_name='assignments', verbose_name=_('person'))
    function = TreeForeignKey(Function, verbose_name=_('function'))

    start = models.DateField(blank=True, null=True, verbose_name=_('start'), help_text=_('First date of assignment.'))
    end = models.DateField(blank=True, null=True, verbose_name=_('end'), help_text=_('Last date of assignment.'))

    trial = models.BooleanField(default=False, verbose_name=_('trial'))

    objects = AssignmentManager()

    class Meta:
        ordering = ['start']

    def __str__(self):
        return u'{0}: {1}'.format(self.person.get_short_name(), self.function)

    @property
    def membership(self):
        return self.function.membership

    @property
    def engagement(self):
        return self.function.engagement

    @property
    def on_timeline(self):
        return self.function.show_in_timeline

    @property
    def ongoing(self):
        return self.objects.ongoing().filter(pk__in=self.pk).exists()

    def convert_to_regular_membership(self, date=datetime.date.today()):
        a = Assignment(person=self.person, function=self.function, start_date=date, trial=False)
        a.save()

        self.end_date = date
        self.save()

    def convert_to_oldie_membership(self, date):
        pass


@python_2_unicode_compatible
class SpecialDiet(models.Model):
    name = models.CharField(max_length=256, verbose_name=_('name'), help_text=_(u'Anges i formen "Allergisk mot...", "Nykterist" etc.'))

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class CustomerPhoneNumber(PhoneNumber):
    customer = models.ForeignKey('blasbase.Customer', related_name='phone_numbers', verbose_name=_('customer'))


class CustomerEmailAddress(EmailAddress):
    customer = models.ForeignKey('blasbase.Customer', related_name='email_addresses', verbose_name=_('customer'))


@python_2_unicode_compatible
class Customer(AddressMixin, models.Model):
    name = models.CharField(max_length=256, verbose_name=_('name'))
    organisation_number = models.CharField(max_length=12, blank=True, verbose_name=_('organisation number'))
    comments = models.TextField(blank=True, verbose_name=_('comments'))

    contact = models.CharField(max_length=256, blank=True, verbose_name=_('contact person'))

    class Meta:
        ordering = ['name', 'contact']

    def __str__(self):
        return self.name