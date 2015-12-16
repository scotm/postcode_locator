from django.conf.urls import url

from postcode_locator.views import PostcodeMappingView

__author__ = 'scotm'

urlpatterns = [
    url(r'^map$', PostcodeMappingView.as_view(), name='postcode_point'),
]
