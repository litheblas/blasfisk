# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Adding model 'Carousel'
        db.create_table(u'blasstrap_carousel', (
            (u'cmsplugin_ptr',
             self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True,
                                                                      primary_key=True)),
            ('extra_css_classes', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('indicators', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('controls', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('arrows', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('interval', self.gf('django.db.models.fields.IntegerField')(default=5000)),
            ('pause', self.gf('django.db.models.fields.CharField')(default='hover', max_length=64)),
            ('wrap', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'blasstrap', ['Carousel'])

        # Adding model 'CarouselEntry'
        db.create_table(u'blasstrap_carouselentry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('caption_header', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('caption', self.gf('django.db.models.fields.TextField')()),
            ('priority', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'blasstrap', ['CarouselEntry'])

        # Adding model 'Jumbotron'
        db.create_table(u'blasstrap_jumbotron', (
            (u'cmsplugin_ptr',
             self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True,
                                                                      primary_key=True)),
            ('extra_css_classes', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('full_width', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'blasstrap', ['Jumbotron'])


    def backwards(self, orm):
        # Deleting model 'Carousel'
        db.delete_table(u'blasstrap_carousel')

        # Deleting model 'CarouselEntry'
        db.delete_table(u'blasstrap_carouselentry')

        # Deleting model 'Jumbotron'
        db.delete_table(u'blasstrap_jumbotron')


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
            'extra_css_classes': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'full_width': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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