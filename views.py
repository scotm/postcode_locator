# Create your views here.
from json_views.views import JSONDataView

from postcode_locator.models import PostcodeMapping


class PostcodeMappingView(JSONDataView):
    def get_context_data(self, **kwargs):
        context = super(PostcodeMappingView, self).get_context_data(**kwargs)
        mapping = PostcodeMapping.match_postcode(postcode=self.request.GET.get('postcode', None),
                                                 raise_exceptions=False)
        if mapping:
            context.update({'data': mapping.point})
        return context
