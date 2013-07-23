import logging
from urlparse import urljoin

from django.http import HttpResponse
from django.views.generic import View
from requests import request

logger = logging.getLogger(__name__)


class HttpProxy(View):
    base_url = None

    def __init__(self, *args, **kwargs):
        return super(View, self).__init__(*args, **kwargs)

    @property
    def proxy_url(self):
        """Complete URL to the resource to proxy"""
        return urljoin(self.base_url, self.kwargs.get('url', ''))

    def _verify_config(self):
        assert self.base_url, "base_url must be set to generate a proxy url"

    def dispatch(self, request, *args, **kwargs):
        """Dispatch all HTTP methods to the proxy"""
        self._verify_config()

        return self.proxy()

    def proxy(self):
        """Return an HttpResponse built based on retrieving self.proxy_url"""
        result = request(
            method=self.request.method, url=self.proxy_url,
            data=self.request.body, headers=self.request.META,
            cookies=self.request.COOKIES, files=self.request.FILES)

        response = HttpResponse(result.raw, status=result.status_code)

        # Attach headers to response
        for header, value in result.headers.iteritems():
            response[header] = value

        return response
