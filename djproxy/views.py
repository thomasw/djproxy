"""HTTP Reverse Proxy class based generic view."""
from django import get_version as get_django_version
from django.http import HttpResponse
from django.views.generic import View
from requests import request
from six.moves.urllib.parse import urljoin
from six import iteritems

from .headers import HeaderDict
from .proxy_middleware import MiddlewareSet
from .request import DownstreamRequest


class HttpProxy(View):
    """Reverse HTTP Proxy class-based generic view."""

    base_url = None
    ignored_upstream_headers = [
        'Content-Length', 'Content-Encoding', 'Keep-Alive', 'Connection',
        'Transfer-Encoding', 'Host', 'Expect', 'Upgrade']
    ignored_request_headers = [
        'Content-Length', 'Content-Encoding', 'Keep-Alive', 'Connection',
        'Transfer-Encoding', 'Host', 'Expect', 'Upgrade']
    proxy_middleware = [
        'djproxy.proxy_middleware.AddXFF',
        'djproxy.proxy_middleware.AddXFH',
        'djproxy.proxy_middleware.AddXFP',
        'djproxy.proxy_middleware.ProxyPassReverse'
    ]
    pass_query_string = True
    reverse_urls = []
    verify_ssl = True
    cert = None
    timeout = None

    @property
    def proxy_url(self):
        """Return URL to the resource to proxy."""
        return urljoin(self.base_url, self.kwargs.get('url', ''))

    def _verify_config(self):
        assert self.base_url, 'base_url must be set to generate a proxy url'

        for rule in self.reverse_urls:
            assert len(rule) == 2, 'reverse_urls must be 2 string iterables'

        iter(self.ignored_upstream_headers)
        iter(self.ignored_request_headers)
        iter(self.proxy_middleware)

    def dispatch(self, request, *args, **kwargs):
        """Dispatch all HTTP methods to the proxy."""
        self.request = DownstreamRequest(request)
        self.args = args
        self.kwargs = kwargs

        self._verify_config()

        self.middleware = MiddlewareSet(self.proxy_middleware)

        return self.proxy()

    def proxy(self):
        """Retrieve the upstream content and build an HttpResponse."""
        headers = self.request.headers.filter(self.ignored_request_headers)
        qs = self.request.query_string if self.pass_query_string else ''

        # Fix for django 1.10.0 bug https://code.djangoproject.com/ticket/27005
        if (self.request.META.get('CONTENT_LENGTH', None) == '' and
                get_django_version() == '1.10'):
            del self.request.META['CONTENT_LENGTH']

        request_kwargs = self.middleware.process_request(
            self, self.request, method=self.request.method, url=self.proxy_url,
            headers=headers, data=self.request.body, params=qs,
            allow_redirects=False, verify=self.verify_ssl, cert=self.cert,
            timeout=self.timeout)

        result = request(**request_kwargs)

        response = HttpResponse(result.content, status=result.status_code)

        # Attach forwardable headers to response
        forwardable_headers = HeaderDict(result.headers).filter(
            self.ignored_upstream_headers)
        for header, value in iteritems(forwardable_headers):
            response[header] = value

        return self.middleware.process_response(
            self, self.request, result, response)
