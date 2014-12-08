from django.contrib.gis.geos import Point
from django.test import TestCase

from postcode_locator.models import PostcodeMapping


class MatchPostcodeTest(TestCase):
    def setUp(self):
        pass

    def test_match_postcode(self):
        point = Point(-3.1627269999999998, 55.9735760000000013)
        p = PostcodeMapping(postcode='EH67HQ', point=point)
        p.save()
        with self.assertRaises(PostcodeMapping.DoesNotExist):
            PostcodeMapping.match_postcode('')
        with self.assertRaises(PostcodeMapping.DoesNotExist):
            PostcodeMapping.match_postcode('AS2SAD')
        self.assertEqual(PostcodeMapping.match_postcode('EH6 7HQ').point, point)
        self.assertEqual(PostcodeMapping.match_postcode('EH67HQ').point, point)
        self.assertEqual(PostcodeMapping.match_postcode('EH6  7HQ').point, point)
