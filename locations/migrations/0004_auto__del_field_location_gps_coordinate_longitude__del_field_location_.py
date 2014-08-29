# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Location.gps_coordinate_longitude'
        db.delete_column(u'locations_location', 'gps_coordinate_longitude')

        # Deleting field 'Location.gps_coordinate_latitude'
        db.delete_column(u'locations_location', 'gps_coordinate_latitude')

        # Adding field 'Location.latitude'
        db.add_column(u'locations_location', 'latitude',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=9, blank=True),
                      keep_default=False)

        # Adding field 'Location.longitude'
        db.add_column(u'locations_location', 'longitude',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=9, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Location.gps_coordinate_longitude'
        db.add_column(u'locations_location', 'gps_coordinate_longitude',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Location.gps_coordinate_latitude'
        db.add_column(u'locations_location', 'gps_coordinate_latitude',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Location.latitude'
        db.delete_column(u'locations_location', 'latitude')

        # Deleting field 'Location.longitude'
        db.delete_column(u'locations_location', 'longitude')


    models = {
        u'locations.location': {
            'Meta': {'object_name': 'Location'},
            '_display_name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "'SE'", 'max_length': '2', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '9', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '9', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'post_code': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'})
        }
    }

    complete_apps = ['locations']