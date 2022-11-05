# The django url function is deprecated as of django 3.1
# We use its equivalent re_path to maintain compatibility
# with older versions of django
try:
    from django.urls import re_path
except ImportError as exception:
    from django.conf.urls import url as re_path


from djproxy.urls import generate_routes
from .test_views import LocalProxy, QuickTimeoutProxy, index


urlpatterns = [
    re_path(r'^some/content/.*$', index, name='index'),
    re_path(r'^local_proxy/(?P<url>.*)$', LocalProxy.as_view(), name='proxy'),
    re_path(r'^quick/(?P<url>.*)$', QuickTimeoutProxy.as_view(), name='proxy'),
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
