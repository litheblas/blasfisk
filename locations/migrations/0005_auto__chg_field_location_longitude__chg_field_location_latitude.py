# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Location.longitude'
        db.alter_column(u'locations_location', 'longitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=18, decimal_places=15))

        # Changing field 'Location.latitude'
        db.alter_column(u'locations_location', 'latitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=18, decimal_places=15))

    def backwards(self, orm):

        # Changing field 'Location.longitude'
        db.alter_column(u'locations_location', 'longitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=9))

        # Changing field 'Location.latitude'
        db.alter_column(u'locations_location', 'latitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=9))

    models = {
        u'locations.location': {
            'Meta': {'object_name': 'Location'},
            '_display_name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "'SE'", 'max_length': '2', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '18', 'decimal_places': '15', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '18', 'decimal_places': '15', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'post_code': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'})
        }
    }

    complete_apps = ['locations']