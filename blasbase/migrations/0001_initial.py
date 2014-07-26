# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PersonPhoneNumber'
        db.create_table(u'blasbase_personphonenumber', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(default='private', max_length=16)),
            ('country', self.gf('django.db.models.fields.CharField')(default='SE', max_length=2, blank=True)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='phone_numbers', to=orm['blasbase.Person'])),
        ))
        db.send_create_signal(u'blasbase', ['PersonPhoneNumber'])

        # Adding model 'CustomerPhoneNumber'
        db.create_table(u'blasbase_customerphonenumber', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(default='private', max_length=16)),
            ('country', self.gf('django.db.models.fields.CharField')(default='SE', max_length=2, blank=True)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='phone_numbers', to=orm['blasbase.Customer'])),
        ))
        db.send_create_signal(u'blasbase', ['CustomerPhoneNumber'])

        # Adding model 'PersonEmailAddress'
        db.create_table(u'blasbase_personemailaddress', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(default='private', max_length=16)),
            ('email_address', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='email_addresses', to=orm['blasbase.Person'])),
        ))
        db.send_create_signal(u'blasbase', ['PersonEmailAddress'])

        # Adding model 'CustomerEmailAddress'
        db.create_table(u'blasbase_customeremailaddress', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(default='private', max_length=16)),
            ('email_address', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='email_addresses', to=orm['blasbase.Customer'])),
        ))
        db.send_create_signal(u'blasbase', ['CustomerEmailAddress'])

        # Adding model 'Person'
        db.create_table(u'blasbase_person', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('post_code', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(default='SE', max_length=2, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('nickname', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('born', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('deceased', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('personal_id_number', self.gf('django.db.models.fields.CharField')(max_length=4, blank=True)),
            ('liu_id', self.gf('django.db.models.fields.CharField')(max_length=8, blank=True)),
            ('about', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('special_diets_extra', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'blasbase', ['Person'])

        # Adding M2M table for field special_diets on 'Person'
        m2m_table_name = db.shorten_name(u'blasbase_person_special_diets')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('person', models.ForeignKey(orm[u'blasbase.person'], null=False)),
            ('specialdiet', models.ForeignKey(orm[u'blasbase.specialdiet'], null=False))
        ))
        db.create_unique(m2m_table_name, ['person_id', 'specialdiet_id'])

        # Adding model 'Avatar'
        db.create_table(u'blasbase_avatar', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('picture', self.gf('imagekit.models.fields.ProcessedImageField')(max_length=100)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='avatars', to=orm['blasbase.Person'])),
            ('primary', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'blasbase', ['Avatar'])

        # Adding model 'User'
        db.create_table(u'blasbase_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=256, db_index=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('person', self.gf('django.db.models.fields.related.OneToOneField')(related_name='user', unique=True, to=orm['blasbase.Person'])),
        ))
        db.send_create_signal(u'blasbase', ['User'])

        # Adding M2M table for field groups on 'User'
        m2m_table_name = db.shorten_name(u'blasbase_user_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm[u'blasbase.user'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['user_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'User'
        m2m_table_name = db.shorten_name(u'blasbase_user_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm[u'blasbase.user'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['user_id', 'permission_id'])

        # Adding model 'Function'
        db.create_table(u'blasbase_function', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['blasbase.Function'])),
            ('membership', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('engagement', self.gf('django.db.models.fields.BooleanField')(default=False)),
            (u'lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'blasbase', ['Function'])

        # Adding unique constraint on 'Function', fields ['parent', 'name']
        db.create_unique(u'blasbase_function', ['parent_id', 'name'])

        # Adding M2M table for field permissions on 'Function'
        m2m_table_name = db.shorten_name(u'blasbase_function_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('function', models.ForeignKey(orm[u'blasbase.function'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['function_id', 'permission_id'])

        # Adding model 'Section'
        db.create_table(u'blasbase_section', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'blasbase', ['Section'])

        # Adding M2M table for field permissions on 'Section'
        m2m_table_name = db.shorten_name(u'blasbase_section_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('section', models.ForeignKey(orm[u'blasbase.section'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['section_id', 'permission_id'])

        # Adding model 'Post'
        db.create_table(u'blasbase_post', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='posts', null=True, to=orm['blasbase.Section'])),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('membership', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('engagement', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('show_in_timeline', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'blasbase', ['Post'])

        # Adding unique constraint on 'Post', fields ['section', 'name']
        db.create_unique(u'blasbase_post', ['section_id', 'name'])

        # Adding M2M table for field permissions on 'Post'
        m2m_table_name = db.shorten_name(u'blasbase_post_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('post', models.ForeignKey(orm[u'blasbase.post'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['post_id', 'permission_id'])

        # Adding model 'Assignment'
        db.create_table(u'blasbase_assignment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='assignments', to=orm['blasbase.Person'])),
            ('function', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blasbase.Function'])),
            ('start', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('end', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('trial', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'blasbase', ['Assignment'])

        # Adding model 'SpecialDiet'
        db.create_table(u'blasbase_specialdiet', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'blasbase', ['SpecialDiet'])

        # Adding model 'Customer'
        db.create_table(u'blasbase_customer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('post_code', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(default='SE', max_length=2, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('organisation_number', self.gf('django.db.models.fields.CharField')(max_length=12, blank=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('contact', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
        ))
        db.send_create_signal(u'blasbase', ['Customer'])


    def backwards(self, orm):
        # Removing unique constraint on 'Post', fields ['section', 'name']
        db.delete_unique(u'blasbase_post', ['section_id', 'name'])

        # Deleting model 'PersonPhoneNumber'
        db.delete_table(u'blasbase_personphonenumber')

        # Deleting model 'CustomerPhoneNumber'
        db.delete_table(u'blasbase_customerphonenumber')

        # Deleting model 'PersonEmailAddress'
        db.delete_table(u'blasbase_personemailaddress')

        # Deleting model 'CustomerEmailAddress'
        db.delete_table(u'blasbase_customeremailaddress')

        # Deleting model 'Person'
        db.delete_table(u'blasbase_person')

        # Removing M2M table for field special_diets on 'Person'
        db.delete_table(db.shorten_name(u'blasbase_person_special_diets'))

        # Deleting model 'Avatar'
        db.delete_table(u'blasbase_avatar')

        # Deleting model 'User'
        db.delete_table(u'blasbase_user')

        # Removing M2M table for field groups on 'User'
        db.delete_table(db.shorten_name(u'blasbase_user_groups'))

        # Removing M2M table for field user_permissions on 'User'
        db.delete_table(db.shorten_name(u'blasbase_user_user_permissions'))

        # Deleting model 'Function'
        db.delete_table(u'blasbase_function')

        # Removing M2M table for field permissions on 'Function'
        db.delete_table(db.shorten_name(u'blasbase_function_permissions'))

        # Deleting model 'Section'
        db.delete_table(u'blasbase_section')

        # Removing M2M table for field permissions on 'Section'
        db.delete_table(db.shorten_name(u'blasbase_section_permissions'))

        # Deleting model 'Post'
        db.delete_table(u'blasbase_post')

        # Removing M2M table for field permissions on 'Post'
        db.delete_table(db.shorten_name(u'blasbase_post_permissions'))

        # Deleting model 'Assignment'
        db.delete_table(u'blasbase_assignment')

        # Deleting model 'SpecialDiet'
        db.delete_table(u'blasbase_specialdiet')

        # Deleting model 'Customer'
        db.delete_table(u'blasbase_customer')


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
            'Meta': {'ordering': "['start']", 'object_name': 'Assignment'},
            'end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'function': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['blasbase.Function']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'assignments'", 'to': u"orm['blasbase.Person']"}),
            'start': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'trial': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'blasbase.avatar': {
            'Meta': {'ordering': "['primary', 'id']", 'object_name': 'Avatar'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'avatars'", 'to': u"orm['blasbase.Person']"}),
            'picture': ('imagekit.models.fields.ProcessedImageField', [], {'max_length': '100'}),
            'primary': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
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
        u'blasbase.customeremailaddress': {
            'Meta': {'object_name': 'CustomerEmailAddress'},
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'email_addresses'", 'to': u"orm['blasbase.Customer']"}),
            'email_address': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'private'", 'max_length': '16'})
        },
        u'blasbase.customerphonenumber': {
            'Meta': {'object_name': 'CustomerPhoneNumber'},
            'country': ('django.db.models.fields.CharField', [], {'default': "'SE'", 'max_length': '2', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'phone_numbers'", 'to': u"orm['blasbase.Customer']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'private'", 'max_length': '16'})
        },
        u'blasbase.function': {
            'Meta': {'unique_together': "(('parent', 'name'),)", 'object_name': 'Function'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'engagement': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'membership': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['blasbase.Function']"}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False'}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'blasbase.person': {
            'Meta': {'ordering': "['first_name', 'last_name', 'nickname']", 'object_name': 'Person'},
            'about': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'born': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "'SE'", 'max_length': '2', 'blank': 'True'}),
            'deceased': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'functions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['blasbase.Function']", 'through': u"orm['blasbase.Assignment']", 'symmetrical': 'False'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'liu_id': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'personal_id_number': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'post_code': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'special_diets': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'people'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['blasbase.SpecialDiet']"}),
            'special_diets_extra': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'})
        },
        u'blasbase.personemailaddress': {
            'Meta': {'object_name': 'PersonEmailAddress'},
            'email_address': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'email_addresses'", 'to': u"orm['blasbase.Person']"}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'private'", 'max_length': '16'})
        },
        u'blasbase.personphonenumber': {
            'Meta': {'object_name': 'PersonPhoneNumber'},
            'country': ('django.db.models.fields.CharField', [], {'default': "'SE'", 'max_length': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'phone_numbers'", 'to': u"orm['blasbase.Person']"}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'private'", 'max_length': '16'})
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
        u'blasbase.user': {
            'Meta': {'ordering': "['person', 'username']", 'object_name': 'User'},
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'person': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'user'", 'unique': 'True', 'to': u"orm['blasbase.Person']"}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256', 'db_index': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['blasbase']