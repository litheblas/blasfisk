# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    depends_on = (
        ("locations", "0001_initial"),
    )

    def forwards(self, orm):
        # Adding model 'EventType'
        db.create_table(u'events_eventtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'events', ['EventType'])

        # Adding model 'Attendance'
        db.create_table(u'events_attendance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Event'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blasbase.Person'])),
            ('answer', self.gf('django.db.models.fields.CharField')(max_length=8, blank=True)),
        ))
        db.send_create_signal(u'events', ['Attendance'])

        # Adding model 'Event'
        db.create_table(u'events_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('end', self.gf('django.db.models.fields.DateTimeField')()),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['locations.Location'], null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.EventType'])),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blasbase.Customer'])),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
        ))
        db.send_create_signal(u'events', ['Event'])

        # Adding model 'TargetedInfo'
        db.create_table(u'events_targetedinfo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Event'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.Group'])),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'events', ['TargetedInfo'])


    def backwards(self, orm):
        # Deleting model 'EventType'
        db.delete_table(u'events_eventtype')

        # Deleting model 'Attendance'
        db.delete_table(u'events_attendance')

        # Deleting model 'Event'
        db.delete_table(u'events_event')

        # Deleting model 'TargetedInfo'
        db.delete_table(u'events_targetedinfo')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'blasbase.assignment': {
            'Meta': {'ordering': "['start_date']", 'object_name': 'Assignment'},
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'assignments'", 'to': u"orm['blasbase.Person']"}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['blasbase.Post']"}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'trial': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'blasbase.customer': {
            'Meta': {'ordering': "['name', 'contact']", 'object_name': 'Customer'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'contact': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "'SE'", 'max_length': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'organisation_number': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'}),
            'post_code': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'})
        },
        u'blasbase.person': {
            'Meta': {'ordering': "['first_name', 'last_name', 'nickname']", 'object_name': 'Person'},
            'about': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'born': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'deceased': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'liu_id': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'personal_id_number': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'posts': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['blasbase.Post']", 'through': u"orm['blasbase.Assignment']", 'symmetrical': 'False'}),
            'special_diets': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'people'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['blasbase.SpecialDiet']"}),
            'special_diets_extra': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'})
        },
        u'blasbase.post': {
            'Meta': {'ordering': "['section', 'name']", 'unique_together': "(('section', 'name'),)", 'object_name': 'Post'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'engagement': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'membership': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'posts'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.Permission']"}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'posts'", 'null': 'True', 'to': u"orm['blasbase.Section']"}),
            'show_in_timeline': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'blasbase.section': {
            'Meta': {'ordering': "['name']", 'object_name': 'Section'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'sections'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.Permission']"})
        },
        u'blasbase.specialdiet': {
            'Meta': {'ordering': "['name']", 'object_name': 'SpecialDiet'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'events.attendance': {
            'Meta': {'object_name': 'Attendance'},
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['events.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['blasbase.Person']"})
        },
        u'events.event': {
            'Meta': {'object_name': 'Event'},
            'attendees': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['blasbase.Person']", 'through': u"orm['events.Attendance']", 'symmetrical': 'False'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['blasbase.Customer']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['locations.Location']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['events.EventType']"})
        },
        u'events.eventtype': {
            'Meta': {'object_name': 'EventType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'events.targetedinfo': {
            'Meta': {'object_name': 'TargetedInfo'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['events.Event']"}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'locations.location': {
            'Meta': {'object_name': 'Location'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "'SE'", 'max_length': '2', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'gps_coordinate_latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'gps_coordinate_longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'post_code': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'})
        }
    }

    complete_apps = ['events']