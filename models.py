__author__ = 'scotm'
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point


class PostcodeMapping(models.Model):
    postcode = models.CharField(max_length=10, primary_key=True)

    # GeoDjango-specific declarations
    point = models.PointField()
    scraped = models.BooleanField(default=False, db_index=True)

    def __unicode__(self):
        return self.postcode

    @staticmethod
    def match_postcode(postcode):
        return PostcodeMapping.objects.get(postcode=postcode.replace(' ', ''))

    @staticmethod
    def make_postcodemapping(postcode, lat, long):
        return PostcodeMapping(postcode=postcode, point=Point(long, lat))

    objects = models.GeoManager()