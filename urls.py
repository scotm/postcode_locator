from django.conf.urls import url

__author__ = 'scotm'

urlpatterns = [
    url(r'^map$', 'postcode_locator.views.postcodemapping_json_view', name='postcode_point'),
]
