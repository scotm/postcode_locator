__author__ = 'scotm'
import string
from random import uniform, randint, choice

import factory
from django.contrib.gis.geos import Point

from postcode_locator.models import PostcodeMapping


class PostcodeMappingFactory(factory.DjangoModelFactory):
    class Meta:
        model = PostcodeMapping

    postcode = factory.LazyAttribute(
        lambda: "DD%d%d%s" % (randint(1, 8), randint(1, 8), "".join(choice(string.ascii_uppercase) for x in range(2))))
    point = Point(uniform(-2.937769889831543, -2.9126644134521484), uniform(56.4740473445564, 56.47997257534551))
