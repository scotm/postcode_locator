# Create your views here.
from django.http import JsonResponse

from postcode_locator.models import PostcodeMapping


def postcodemapping_json_view(request):
    mapping = PostcodeMapping.match_postcode(postcode=request.GET.get('postcode', None),
                                             raise_exceptions=False)
    data = {'outcome': 'fail'}
    if mapping:
        data = {'outcome': 'success', 'point': [mapping.point.x, mapping.point.y]}
    return JsonResponse(data=data)
