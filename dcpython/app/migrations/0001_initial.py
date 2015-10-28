# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import localflavor.us.models
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField()),
                ('type', models.CharField(max_length=1, choices=[(b'C', b'Credit Card'), (b'G', b'Pledge')])),
                ('completed', models.BooleanField(default=False)),
                ('donation', models.DecimalField(max_digits=10, decimal_places=2)),
                ('transaction_id', models.CharField(max_length=50)),
                ('valid_until', models.DateField(null=True, blank=True)),
                ('level', models.CharField(blank=True, max_length=1, null=True, choices=[(b'A', b'Andrew W. Singer Memorial Level ($2500)'), (b'P', b'Platinum ($1000)'), (b'G', b'Gold ($500)'), (b'S', b'Silver ($250)'), (b'B', b'Bronze ($100)'), (b'I', b'Individual ($50)'), (b'O', b'Other ($0)')])),
                ('reviewed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Donor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=254)),
                ('phone', localflavor.us.models.PhoneNumberField(max_length=20, null=True, blank=True)),
                ('name', models.CharField(help_text=b"If institutional donation, point of contact's name", max_length=100)),
                ('public_name', models.CharField(max_length=100, null=True, verbose_name=b'Display Name', blank=True)),
                ('public_url', models.URLField(null=True, verbose_name=b'Display Url', blank=True)),
                ('public_slogan', models.CharField(max_length=200, null=True, verbose_name=b'Display Slogan', blank=True)),
                ('public_logo', models.ImageField(storage=django.core.files.storage.FileSystemStorage(), upload_to=b'donor_logos', null=True, verbose_name=b'Display Logo', blank=True)),
                ('level', models.CharField(blank=True, max_length=1, null=True, help_text=b"Override levels specified by donations if not past 'valid until'", choices=[(b'A', b'Andrew W. Singer Memorial Level ($2500)'), (b'P', b'Platinum ($1000)'), (b'G', b'Gold ($500)'), (b'S', b'Silver ($250)'), (b'B', b'Bronze ($100)'), (b'I', b'Individual ($50)'), (b'O', b'Other ($0)')])),
                ('secret', models.CharField(max_length=90)),
                ('reviewed', models.BooleanField(default=False)),
                ('valid_until', models.DateField(help_text=b'Specify a date until which the level specified for the donor is valid. After, donation levels will control.', null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('record_created', models.DateTimeField(auto_now_add=True)),
                ('record_modified', models.DateTimeField(auto_now=True)),
                ('meetup_id', models.CharField(unique=True, max_length=32)),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200)),
                ('start_time', models.DateTimeField(null=True)),
                ('end_time', models.DateTimeField(null=True, blank=True)),
                ('meetup_url', models.URLField(blank=True)),
                ('description', models.TextField(null=True, blank=True)),
            ],
            options={
                'ordering': ('start_time', 'end_time'),
                'get_latest_by': 'start_time',
            },
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('remote_id', models.CharField(max_length=100, null=True, blank=True)),
                ('updated', models.CharField(max_length=30)),
                ('event', models.ForeignKey(related_name='playlists', to='app.Event')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceSync',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('service', models.CharField(max_length=200)),
                ('last_synced', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('meetup_id', models.CharField(unique=True, max_length=32)),
                ('lon', models.DecimalField(null=True, max_digits=9, decimal_places=6)),
                ('lat', models.DecimalField(null=True, max_digits=9, decimal_places=6)),
                ('name', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=2)),
                ('address_1', models.CharField(max_length=200)),
                ('address_2', models.CharField(max_length=200, blank=True)),
                ('address_3', models.CharField(max_length=200, blank=True)),
                ('phone', models.CharField(default=b'', max_length=15, blank=True)),
                ('city', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=2)),
                ('zip_code', models.CharField(max_length=5, blank=True)),
                ('repinned', models.BooleanField()),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='venue',
            field=models.ForeignKey(blank=True, to='app.Venue', null=True),
        ),
        migrations.AddField(
            model_name='donation',
            name='donor',
            field=models.ForeignKey(related_name='donations', to='app.Donor'),
        ),
        migrations.AlterUniqueTogether(
            name='event',
            unique_together=set([('start_time', 'slug')]),
        ),
    ]
