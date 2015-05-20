from django.conf.urls import patterns, url

from djproxy.urls import generate_routes
from test_views import index, LocalProxy


urlpatterns = patterns(
    '',
    url(r'^$', index, name='index'),
    url(r'^some/content/.*$', index, name='some_content'),
    url(r'^local_proxy/(?P<url>.*)$', LocalProxy.as_view(), name='proxy'),
) + generate_routes({
    'service_one': {
        'base_url': 'https://www.yahoo.com/',
        'prefix': '/yahoo/',
        'stream': True
    },
    'service_two': {
        'base_url': 'https://www.google.com/',
        'prefix': '/google/',
    },
    'service_three': {
        'base_url': 'http://big.faker/',
        'prefix': '/fakey/',
        'csrf_exempt': False
    },
    'service_four': {
        'base_url': 'https://stream.twitter.com/',
        'prefix': '/twitter/',
        'stream': True
    },
    'service_five': {
        'base_url': 'https://www.yahoo.com/',
        'prefix': '/yahoo-nostream/'
    },
    'httpbin': {
        'base_url': 'http://httpbin.org/',
        'prefix': '/httpbin/'
    },
    'httpbin-stream': {
        'base_url': 'http://httpbin.org/',
        'prefix': '/httpbin-stream/',
        'stream': True
    },
})
