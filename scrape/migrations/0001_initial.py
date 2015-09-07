# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CombativesUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=None, unique=True, max_length=50)),
                ('description', models.CharField(max_length=140, blank=True)),
                ('is_scraped', models.BooleanField(default=False, verbose_name=b'Auto Generated')),
                ('email', models.EmailField(max_length=254)),
                ('website', models.URLField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='OpenHours',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day_num', models.IntegerField(help_text=b'0-Monday, 6-Sunday', choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)])),
                ('start_at', models.TimeField()),
                ('end_at', models.TimeField()),
                ('open_hours', models.ForeignKey(default=None, to='scrape.OpenHours', null=True)),
                ('user', models.ForeignKey(to='scrape.CombativesUser')),
            ],
        ),
    ]
