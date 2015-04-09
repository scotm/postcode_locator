# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations
import random

def add_jitter(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    points = set()
    postcode_mapping_klass = apps.get_model("postcode_locator", "PostcodeMapping")
    for mapping in postcode_mapping_klass.objects.all():
        point = mapping.point.x, mapping.point.y
        while True:
            if point not in points:
                points.add(point)
                break
            point = point[0] + random.uniform(0.0001, 0.0002), point[1]
        if point[0] != mapping.point.x:
            mapping.point.x = point[0]
            mapping.save()

class Migration(migrations.Migration):


    dependencies = [
        ('postcode_locator', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_jitter),
    ]
