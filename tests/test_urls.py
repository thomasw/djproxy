from django.conf.urls import patterns, url

from djproxy.urls import generate_routes
from test_views import LocalProxy, index


urlpatterns = patterns(
    '',
    url(r'^some/content/.*$', index, name='index'),
    url(r'^local_proxy/(?P<url>.*)$', LocalProxy.as_view(), name='proxy')
) + generate_routes({
    'service_one': {
        'base_url': 'https://yahoo.com/',
        'prefix': '/yahoo/'
    },
    'service_two': {
        'base_url': 'http://www.google.com/',
        'prefix': '/google/'
    }
})
