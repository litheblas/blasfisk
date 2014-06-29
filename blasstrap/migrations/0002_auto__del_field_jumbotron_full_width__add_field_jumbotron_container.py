# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Deleting field 'Jumbotron.full_width'
        db.delete_column(u'blasstrap_jumbotron', 'full_width')

        # Adding field 'Jumbotron.container'
        db.add_column(u'blasstrap_jumbotron', 'container',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Jumbotron.full_width'
        db.add_column(u'blasstrap_jumbotron', 'full_width',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Deleting field 'Jumbotron.container'
        db.delete_column(u'blasstrap_jumbotron', 'container')


    models = {
        u'blasstrap.carousel': {
            'Meta': {'object_name': 'Carousel', '_ormbases': ['cms.CMSPlugin']},
            'arrows': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [],
                               {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'controls': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'extra_css_classes': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'indicators': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'interval': ('django.db.models.fields.IntegerField', [], {'default': '5000'}),
            'pause': ('django.db.models.fields.CharField', [], {'default': "'hover'", 'max_length': '64'}),
            'wrap': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'blasstrap.carouselentry': {
            'Meta': {'object_name': 'CarouselEntry'},
            'caption': ('django.db.models.fields.TextField', [], {}),
            'caption_header': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'priority': ('django.db.models.fields.IntegerField', [], {})
        },
        u'blasstrap.jumbotron': {
            'Meta': {'object_name': 'Jumbotron', '_ormbases': ['cms.CMSPlugin']},
            u'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [],
                               {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'container': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'extra_css_classes': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'})
        },
        'cms.cmsplugin': {
            'Meta': {'object_name': 'CMSPlugin'},
            'changed_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [],
                       {'to': "orm['cms.CMSPlugin']", 'null': 'True', 'blank': 'True'}),
            'placeholder': (
            'django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
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
        }
    }

    complete_apps = ['blasstrap']