from django.conf.urls import patterns, url

from test_views import LocalProxy, index


urlpatterns = patterns(
    '',
    url(r'^some/content/.*$', index, name='index'),
    url(r'^local_proxy/(?P<url>.*)$', LocalProxy.as_view(), name='proxy')
)
