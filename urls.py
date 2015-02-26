from postcode_locator.views import PostcodeMappingView

__author__ = 'scotm'
from django.conf.urls import patterns, url


urlpatterns = patterns('',
                       url(r'^map$', PostcodeMappingView.as_view()),
)
