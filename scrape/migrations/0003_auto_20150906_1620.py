# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrape', '0002_auto_20150906_1619'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpenHours',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.AddField(
            model_name='reservation',
            name='open_hours',
            field=models.ForeignKey(default=None, to='scrape.OpenHours', null=True),
        ),
    ]
