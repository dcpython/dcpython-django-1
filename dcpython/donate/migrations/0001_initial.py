# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Donor'
        db.create_table(u'donate_donor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('phone', self.gf('localflavor.us.models.PhoneNumberField')(max_length=20, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('public_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('public_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('public_slogan', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('public_logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('level', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('secret', self.gf('django.db.models.fields.CharField')(max_length=90)),
            ('reviewed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('valid_until', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'donate', ['Donor'])

        # Adding model 'Donation'
        db.create_table(u'donate_donation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('donor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='donations', to=orm['donate.Donor'])),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('completed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('donation', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('transaction_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('valid_until', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('level', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('reviewed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'donate', ['Donation'])


    def backwards(self, orm):
        # Deleting model 'Donor'
        db.delete_table(u'donate_donor')

        # Deleting model 'Donation'
        db.delete_table(u'donate_donation')


    models = {
        u'donate.donation': {
            'Meta': {'object_name': 'Donation'},
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'donation': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'donor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'donations'", 'to': u"orm['donate.Donor']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'reviewed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'transaction_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'valid_until': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        u'donate.donor': {
            'Meta': {'object_name': 'Donor'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone': ('localflavor.us.models.PhoneNumberField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'public_logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'public_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'public_slogan': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'public_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'reviewed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'secret': ('django.db.models.fields.CharField', [], {'max_length': '90'}),
            'valid_until': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['donate']
