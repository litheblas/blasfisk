# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from blasbase.models import Person, SpecialDiet, PersonAddress
from datetime import datetime
import MySQLdb

class Command(BaseCommand):
    help = 'Syncronizes persons from mysql'

    def handle(self, *args, **options):
        gluten = SpecialDiet.objects.get_or_create(name='Glutenallergi')[0]
        veg = SpecialDiet.objects.get_or_create(name='Vegetarian')[0]
        nykter = SpecialDiet.objects.get_or_create(name='Nykterist')[0]
        print u"Öppnar mysqldatabasen"
        db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="blasare", # your username
                      passwd="bajsare", # your password
                      db="litheblas",
                      port=3307,
                      charset='utf8' ) # name of the data base
        print u"Hämtar data från mysql"
        cur = db.cursor()
        cur.execute("SELECT fnamn,smek,enamn,kon,fodd,pnr_sista,studentid,fritext,allergi,gluten,veg,nykter,gatuadr,postnr,ort,land FROM person")
        for row in cur.fetchall() :
            person = Person()
            person.first_name = row[0]
            if row[1]:
                person.nickname = row[1]
            else:
                person.nickname = ""
            person.last_name = row[2]
            if row[3] == 'M':
                person.gender = 'm'
            elif row[3] == 'K':
                person.gender = 'f'
            else:
                person.gender = ""
            person.born = row[4]
            person.deceased = None
            if row[5]:
                person.personal_id_number = row[5]
            else:
                person.personal_id_number = ""
            if row[6]:
                person.liu_id = row[6]
            else:
                person.liu_id = ""
            if row[7]:
                person.about = row[7]
            else:
                person.about = ""
            if row[8]:
                person.special_diets_extra = row[8]
            else:
                person.special_diets_extra = ""
            person.save()
            if row[9] == 'Y':
                person.special_diets.add(gluten)
            if row[10] == 'Y':
                person.special_diets.add(veg)
            if row[11] == 'Y':
                person.special_diets.add(nykter)
            paddress = PersonAddress()
            paddress.type = 'private'
            paddress.person = person
            if row[12]:
                paddress.address = row[12]
            else:
                paddress.address = ""
            if row[13]:
                paddress.post_code = row[13]
            else:
                paddress.post_code = ""
            if row[14]:
                paddress.city = row[14]
            else:
                paddress.city = ""
            if row[15]:
                paddress.country = row[15]
            else:
                paddress.country = ""
            paddress.save()

            """Not yet added """
            """
               test.posts
               """
            person.save()






