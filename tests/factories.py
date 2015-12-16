__author__ = 'scotm'
import string
from random import uniform, randint, choice

import factory
from django.contrib.gis.geos import Point

from postcode_locator.models import PostcodeMapping

latitudes = (56.4740473445564, 56.47997257534551)
longitudes = (-2.937769889831543, -2.9126644134521484)
northeast = (latitudes[1], longitudes[1])
southwest = (latitudes[0], longitudes[0])

class PostcodeMappingFactory(factory.DjangoModelFactory):
    class Meta:
        model = PostcodeMapping
        django_get_or_create = ('postcode',)

    postcode = factory.LazyAttribute(lambda x: "DD%d%d%s" % (
        randint(1, 8), randint(1, 8), "".join(choice(string.ascii_uppercase) for x in range(2))))
    point = factory.LazyAttribute(lambda x: Point(uniform(*longitudes),
                                                  uniform(*latitudes)))
