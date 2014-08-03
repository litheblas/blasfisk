#added requirement to BeautifulSoup
from django.test import TestCase
from requests.auth import HTTPBasicAuth
import requests
from BeautifulSoup import BeautifulSoup
from blasbase.models import Person
from blasbassync.management.commands.syncpersons import Command
from django.conf import settings
from sys import stdout
from time import sleep

# Create your tests here.


class PersonMethodsTestCase(TestCase):
    @classmethod
    def setUpClass(self):
        c = Command()
        c.handle()
        print "Collecting pages from litheblas.org"
        total = Person.objects.all().count()
        count = 1
        self.siteList = {}
        for p in Person.objects.all():
            stdout.write("Downloading page %d/%d   \r" % (count, total) )
            stdout.flush()
            count+=1
            r=requests.get('http://www.litheblas.org/internt/blasbas/person.php?id=%s' % p.old_database_id,auth=HTTPBasicAuth(settings.OLD_SITE_USER, settings.OLD_SITE_PASSWORD))
            while r.status_code!=200:
                sleep(0.1)
                r=requests.get('http://www.litheblas.org/internt/blasbas/person.php?id=%s' % p.old_database_id,auth=HTTPBasicAuth(settings.OLD_SITE_USER, settings.OLD_SITE_PASSWORD))
            self.siteList[p.old_database_id] =r
    def setUp(self):
        pass
    def test_person_names(self):
        print "Testing person names"
        count = 1
        total = Person.objects.all().count()
        for p in Person.objects.all():
            stdout.write("Testing Person %d/%d   \r" % (count, total) )
            stdout.flush()
            count+=1
        soup = BeautifulSoup(self.siteList[p.old_database_id].text)
        current = soup.find('b')
        name = current.text.split( )
        fnamn = name[0]
        if len(name)==3:
            smek = name[1][1:-1]
            enamn = name[2]
        else:
            smek = ""
            enamn = name[1]
        self.assertEquals(fnamn,p.first_name)
        self.assertEquals(smek,p.nickname)
        self.assertEquals(enamn,p.last_name)
    def test_person_memberships(self):
        print "Testing person memberships"
        count = 1
        total = Person.objects.all().count()
        for p in Person.objects.all():
            stdout.write("Testing Person %d/%d   \r" % (count, total) )
            stdout.flush()
            count+=1
            soup = BeautifulSoup(self.siteList[p.old_database_id].text)
            try:
                current = soup.find(text="Medlemskap").findNext('td')
            except:
                print soup.text


            memberships = []
            while current.text != "":
                #print current.text
                temp = current.text.split( )
                membership = {}
                membership['datum'] = temp[0]
                membership['typ'] = temp[1]
                if len(temp) == 3:
                    membership['instrument'] = temp[2]
                memberships.append(membership)
                current = current.findNext('td').findNext('td')
            new_memberships = p.assignments.filter(function__membership=True).order_by('start')
            for m in memberships:
                if m['typ'] == 'gamling':
                    self.assertTrue(self.contains(new_memberships, lambda x: str(x.end) == m['datum']),msg=p.old_database_id)
                if m['typ'] == 'prov':
                    self.assertTrue(self.contains(new_memberships, lambda x: str(x.start) == m['datum'] and x.trial == True),msg=p.old_database_id)
                if m['typ'] == 'antagen':
                    self.assertTrue(self.contains(new_memberships, lambda x: str(x.start) == m['datum'] and x.trial == False),msg=p.old_database_id)




    def contains(self,list, filter):
        for x in list:
            if filter(x):
                return True
        return False



