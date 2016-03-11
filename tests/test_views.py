from django.http import HttpResponse

from djproxy.views import HttpProxy


class LocalProxy(HttpProxy):
    base_url = 'http://localhost:8000/some/content/'


def index(request):
    return HttpResponse('Some content!', status=200)


class TestProxy(HttpProxy):
    base_url = 'https://google.com/'


class UnverifiedSSLProxy(HttpProxy):
    base_url = 'https://google.com/'
    verify_ssl = False


class QuickTimeoutProxy(HttpProxy):
    base_url = 'https://google.com/'
    verify_ssl = False
    timeout = (0.1, 0.1)


class SpecifiedCertProxy(HttpProxy):
    base_url = 'https://google.com/'
    cert = ('cert.pem', 'key.pem')


class ReverseProxy(HttpProxy):
    base_url = 'https://google.com/'
    reverse_urls = [
        ('/google/', 'https://google.com/')
    ]
