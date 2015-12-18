from django.contrib.gis.geos import Point
from django.core.urlresolvers import reverse
from django.test import TestCase

from postcode_locator.models import PostcodeMapping
from postcode_locator.tests.factories import PostcodeMappingFactory


class MatchPostcodeTest(TestCase):
    def setUp(self):
        pass

    def test_match_postcode(self):
        point = Point(-3.1627269999999998, 55.9735760000000013)
        p = PostcodeMappingFactory(postcode='EH67HQ', point=point)
        with self.assertRaises(PostcodeMapping.DoesNotExist):
            PostcodeMapping.match_postcode('')
        with self.assertRaises(PostcodeMapping.DoesNotExist):
            PostcodeMapping.match_postcode('AS2SAD')
        self.assertEqual(unicode(p), 'EH67HQ')
        self.assertEqual(PostcodeMapping.match_postcode('AS2SAD',raise_exceptions=False), None)
        self.assertEqual(PostcodeMapping.match_postcode('EH6 7HQ').point, point)
        self.assertEqual(PostcodeMapping.match_postcode('EH67HQ').point, point)
        self.assertEqual(PostcodeMapping.match_postcode('EH6  7HQ').point, point)

    def test_postcodemappingfactory(self):
        p = PostcodeMappingFactory.create()
        q = PostcodeMappingFactory.create()
        self.assertNotEqual(p.point, q.point)

    def test_page(self):
        import json
        p = PostcodeMappingFactory.create()
        response = self.client.get(reverse('postcode_point'), data={'postcode':p.pk})
        data = json.loads(response.content)
        self.assertAlmostEqual(data['point'][0], p.point.x,places=6)
        self.assertAlmostEqual(data['point'][1], p.point.y,places=6)

