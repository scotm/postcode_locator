# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PostcodeMapping',
            fields=[
                ('postcode', models.CharField(max_length=10, serialize=False, primary_key=True)),
                ('point', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('scraped', models.BooleanField(default=False, db_index=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
