from django.http import HttpResponse

from djproxy.views import HttpProxy

DOWNSTREAM_INJECTION = lambda x: x


class LocalProxy(HttpProxy):
    base_url = "http://sitebuilder.qa.yola.net/en/ide/Yola/Yola.session.jsp"


class SBProxy(HttpProxy):
    base_url = "http://sitebuilder.qa.yola.net/en/APIController"


def index(request):
    DOWNSTREAM_INJECTION(request)
    return HttpResponse('Some content!', status=200)


class BadTestProxy(HttpProxy):
    pass


class GoodTestProxy(HttpProxy):
    base_url = "https://google.com/"
