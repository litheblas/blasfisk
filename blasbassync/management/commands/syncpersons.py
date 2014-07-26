# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from blasbase.models import Person
import MySQLdb

class Command(BaseCommand):
    help = 'Syncronizes persons from mysql'

    def handle(self, *args, **options):
        print u"Öppnar mysqldatabasen"
        db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="blasare", # your username
                      passwd="bajsare", # your password
                      db="litheblas",
                      port=3307,
                      charset='utf8' ) # name of the data base
        print "Hämtar data från mysql"
        cur = db.cursor()
        cur.execute("SELECT fnamn,smek,enamn,kon FROM person")
        for row in cur.fetchall() :
            test = Person()
            test.first_name = row[0]
            test.nickname = row[1]
            test.last_name = row[2]
            if row[3] == 'M':
                test.gender = 'm'
            elif row[3] == 'K':
                test.gender = 'f'
            else:
                test.gender = None

            print test
            print test.gender





"""class Person(models.Model):
    Lagrar personer (som i människor) och är den datatyp som nästan allt i Blåsbasen kopplas till.

 X   first_name = models.CharField(max_length=256, verbose_name=_('first name'))
 X   nickname = models.CharField(max_length=256, blank=True, verbose_name=_('nickname'))
 X   last_name = models.CharField(max_length=256, verbose_name=_('last name'),
                                 help_text=u'Ange gärna tidigare efternamn inom parentes, t.ex. Vidner (Eriksson)')
 X   gender = models.CharField(max_length=1, choices=GENDERS, blank=True, verbose_name=_('gender'))
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


    posts = models.ManyToManyField('Post', through='Assignment', verbose_name=_('posts'))


    last_updated = models.DateTimeField(auto_now=True, verbose_name=_('last updated'))


    # Låt oss fortsätta kalla den objects istället för typ people, så hålls det konsekvent mellan alla modeller
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
        Hämtar alla assignments som innebär medlemsskap och som inte är provmedlemsskap,
        sorterar stigande på startdatum, tar det första objektet och ger detta objekts startdatum
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
"""


