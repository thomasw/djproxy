from django.http import HttpResponse

from djproxy.views import HttpProxy

DOWNSTREAM_INJECTION = lambda x: x


class LocalProxy(HttpProxy):
    base_url = "http://127.0.0.1:8081/some/content/"


def index(request):
    DOWNSTREAM_INJECTION(request)
    return HttpResponse('Some content!', status=200)


class BadTestProxy(HttpProxy):
    pass


class GoodTestProxy(HttpProxy):
    base_url = "https://google.com/"
