from django.conf.urls import patterns, url
from django.http import HttpResponse
from djproxy.views import HttpProxy


class LocalProxy(HttpProxy):
    base_url = "http://127.0.0.1:8000/some/content/"


def index(request):
    return HttpResponse('Some content!', status=200)


urlpatterns = patterns(
    '',
    url(r'^some/content/.*$', index, name='index'),
    url(r'^local_proxy/(?P<url>.*)$', LocalProxy.as_view(), name='proxy')
)
