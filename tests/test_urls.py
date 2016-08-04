from django.conf.urls import url

from djproxy.urls import generate_routes
from .test_views import LocalProxy, QuickTimeoutProxy, index


urlpatterns = [
    url(r'^some/content/.*$', index, name='index'),
    url(r'^local_proxy/(?P<url>.*)$', LocalProxy.as_view(), name='proxy'),
    url(r'^quick/(?P<url>.*)$', QuickTimeoutProxy.as_view(), name='proxy'),
]

urlpatterns += generate_routes({
    'service_one': {
        'base_url': 'https://www.yahoo.com/',
        'prefix': '/yahoo/'
    },
    'service_two': {
        'base_url': 'http://www.google.com/',
        'prefix': '/google/'
    },
    'service_three': {
        'base_url': 'http://big.faker/',
        'prefix': '/fakey/',
        'csrf_exempt': False
    }
})
