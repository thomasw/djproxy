from django.http import HttpResponse

from djproxy.views import HttpProxy


class LocalProxy(HttpProxy):
    base_url = "http://localhost:8000/some/content/"


def index(request):
    return HttpResponse('Some content!', status=200)


class TestProxy(HttpProxy):
    base_url = "https://google.com/"
