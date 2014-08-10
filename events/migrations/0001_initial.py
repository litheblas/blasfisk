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

        # Adding model 'Contact'
        db.create_table(u'events_contact', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Event'])),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blasbase.Customer'])),
            ('department', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('contact', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True)),
        ))
        db.send_create_signal(u'events', ['Contact'])

        # Adding model 'ContactPhoneNumber'
        db.create_table(u'events_contactphonenumber', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(default='private', max_length=16)),
            ('country', self.gf('django.db.models.fields.CharField')(default='SE', max_length=2, blank=True)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(related_name='phone_numbers', to=orm['events.Contact'])),
        ))
        db.send_create_signal(u'events', ['ContactPhoneNumber'])

        # Adding model 'ContactEmailAddress'
        db.create_table(u'events_contactemailaddress', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(default='private', max_length=16)),
            ('email_address', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(related_name='email_addresses', to=orm['events.Contact'])),
        ))
        db.send_create_signal(u'events', ['ContactEmailAddress'])

        # Adding model 'Event'
        db.create_table(u'events_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('end', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('deadline', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='events', null=True, to=orm['locations.Location'])),
            ('event_type', self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='events', to=orm['events.EventType'])),
            ('cancelled', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'events', ['Event'])

        # Adding M2M table for field visible_to on 'Event'
        m2m_table_name = db.shorten_name(u'events_event_visible_to')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'events.event'], null=False)),
            ('function', models.ForeignKey(orm[u'blasbase.function'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'function_id'])

        # Adding model 'EventInformation'
        db.create_table(u'events_eventinformation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Event'])),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'events', ['EventInformation'])

        # Adding M2M table for field functions on 'EventInformation'
        m2m_table_name = db.shorten_name(u'events_eventinformation_functions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('eventinformation', models.ForeignKey(orm[u'events.eventinformation'], null=False)),
            ('function', models.ForeignKey(orm[u'blasbase.function'], null=False))
        ))
        db.create_unique(m2m_table_name, ['eventinformation_id', 'function_id'])

        # Adding model 'EventViewer'
        db.create_table(u'events_eventviewer', (
            (u'cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('count', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'events', ['EventViewer'])

        # Adding M2M table for field event_types on 'EventViewer'
        m2m_table_name = db.shorten_name(u'events_eventviewer_event_types')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('eventviewer', models.ForeignKey(orm[u'events.eventviewer'], null=False)),
            ('eventtype', models.ForeignKey(orm[u'events.eventtype'], null=False))
        ))
        db.create_unique(m2m_table_name, ['eventviewer_id', 'eventtype_id'])


    def backwards(self, orm):
        # Deleting model 'EventType'
        db.delete_table(u'events_eventtype')

        # Deleting model 'Attendance'
        db.delete_table(u'events_attendance')

        # Deleting model 'Contact'
        db.delete_table(u'events_contact')

        # Deleting model 'ContactPhoneNumber'
        db.delete_table(u'events_contactphonenumber')

        # Deleting model 'ContactEmailAddress'
        db.delete_table(u'events_contactemailaddress')

        # Deleting model 'Event'
        db.delete_table(u'events_event')

        # Removing M2M table for field visible_to on 'Event'
        db.delete_table(db.shorten_name(u'events_event_visible_to'))

        # Deleting model 'EventInformation'
        db.delete_table(u'events_eventinformation')

        # Removing M2M table for field functions on 'EventInformation'
        db.delete_table(db.shorten_name(u'events_eventinformation_functions'))

        # Deleting model 'EventViewer'
        db.delete_table(u'events_eventviewer')

        # Removing M2M table for field event_types on 'EventViewer'
        db.delete_table(db.shorten_name(u'events_eventviewer_event_types'))


    models = {
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'blasbase.assignment': {
            'Meta': {'ordering': "['start']", 'object_name': 'Assignment'},
            'end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'function': ('mptt.fields.TreeForeignKey', [], {'to': u"orm['blasbase.Function']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'assignments'", 'to': u"orm['blasbase.Person']"}),
            'start': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'trial': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'blasbase.customer': {
            'Meta': {'ordering': "['name']", 'unique_together': "(['name', 'organisation_number'],)", 'object_name': 'Customer'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "'SE'", 'max_length': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'organisation_number': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'}),
            'post_code': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'})
        },
        u'blasbase.function': {
            'Meta': {'unique_together': "(('parent', 'name'),)", 'object_name': 'Function'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'engagement': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'membership': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['blasbase.Function']"}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'functions'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.Permission']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'blasbase.person': {
            'Meta': {'ordering': "['first_name', 'last_name', 'nickname']", 'object_name': 'Person'},
            'about': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'born': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'deceased': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'functions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['blasbase.Function']", 'through': u"orm['blasbase.Assignment']", 'symmetrical': 'False'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'liu_id': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'old_database_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'personal_id_number': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'special_diets': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'people'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['blasbase.SpecialDiet']"}),
            'special_diets_extra': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'})
        },
        u'blasbase.specialdiet': {
            'Meta': {'ordering': "['name']", 'object_name': 'SpecialDiet'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'cms.cmsplugin': {
            'Meta': {'object_name': 'CMSPlugin'},
            'changed_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.CMSPlugin']", 'null': 'True', 'blank': 'True'}),
            'placeholder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            'plugin_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'cms.placeholder': {
            'Meta': {'object_name': 'Placeholder'},
            'default_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
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
        u'events.contact': {
            'Meta': {'object_name': 'Contact'},
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'contact': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['blasbase.Customer']"}),
            'department': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['events.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'})
        },
        u'events.contactemailaddress': {
            'Meta': {'object_name': 'ContactEmailAddress'},
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'email_addresses'", 'to': u"orm['events.Contact']"}),
            'email_address': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'private'", 'max_length': '16'})
        },
        u'events.contactphonenumber': {
            'Meta': {'object_name': 'ContactPhoneNumber'},
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'phone_numbers'", 'to': u"orm['events.Contact']"}),
            'country': ('django.db.models.fields.CharField', [], {'default': "'SE'", 'max_length': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'private'", 'max_length': '16'})
        },
        u'events.event': {
            'Meta': {'ordering': "['start']", 'object_name': 'Event'},
            'attendees': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['blasbase.Person']", 'null': 'True', 'through': u"orm['events.Attendance']", 'blank': 'True'}),
            'cancelled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'customer': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['blasbase.Customer']", 'through': u"orm['events.Contact']", 'symmetrical': 'False'}),
            'deadline': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'event_type': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'related_name': "'events'", 'to': u"orm['events.EventType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'events'", 'null': 'True', 'to': u"orm['locations.Location']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'visible_to': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['blasbase.Function']", 'null': 'True', 'blank': 'True'})
        },
        u'events.eventinformation': {
            'Meta': {'object_name': 'EventInformation'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['events.Event']"}),
            'functions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['blasbase.Function']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'events.eventtype': {
            'Meta': {'object_name': 'EventType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'events.eventviewer': {
            'Meta': {'object_name': 'EventViewer', '_ormbases': ['cms.CMSPlugin']},
            u'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'count': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'event_types': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['events.EventType']", 'null': 'True', 'blank': 'True'})
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