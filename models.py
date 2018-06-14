__author__ = 'scotm'
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.db.models import Manager as GeoManager

class PostcodeMapping(models.Model):
    postcode = models.CharField(max_length=10, primary_key=True)

    # GeoDjango-specific declarations
    point = models.PointField()
    scraped = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        return self.postcode

    @staticmethod
    def match_postcode(postcode, raise_exceptions=True):
        try:
            return PostcodeMapping.objects.get(postcode=postcode.replace(' ', ''))
        except PostcodeMapping.DoesNotExist:
            if raise_exceptions:
                raise
            return None

    @staticmethod
    def make_postcodemapping(postcode, lat, long):
        return PostcodeMapping(postcode=postcode, point=Point(long, lat))

    objects = GeoManager()