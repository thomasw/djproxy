import logging
from urlparse import urljoin, urlparse
import socket

from django.http import HttpResponse
from django.views.generic import View
from requests import request

logger = logging.getLogger(__name__)


class HttpProxy(View):
    """Reverse HTTP Proxy class-based generic view."""

    base_url = None
    ignored_downstream_headers = [
        'Content-Length', 'Content-Encoding', 'Keep-Alive', 'Connection',
        'Transfer-Encoding', 'Host', 'Expect', 'Upgrade']
    ignored_request_headers = [
        'Content-Length', 'Content-Encoding', 'Keep-Alive', 'Connection',
        'Transfer-Encoding', 'Host', 'Expect', 'Upgrade']
    pass_query_string = True

    def __init__(self, *args, **kwargs):
        return super(View, self).__init__(*args, **kwargs)

    @property
    def proxy_url(self):
        """Complete URL to the resource to proxy"""
        return urljoin(self.base_url, self.kwargs.get('url', ''))

    @property
    def headers(self):
        """Request headers contained in self.request.META"""
        request_headers = {}
        other_headers = ['CONTENT_TYPE', 'CONTENT_LENGTH']

        for header, value in self.request.META.iteritems():
            is_header = header.startswith('HTTP_') or header in other_headers
            normalized_header = self.normalize_django_header_name(header)

            if is_header and value:
                request_headers[normalized_header] = value

        return request_headers

    @property
    def downstream_ip(self):
        """IP address of the resource to be proxied."""
        return socket.gethostbyname(urlparse(self.proxy_url).hostname)

    @property
    def query_string(self):
        """Incoming request's query string"""
        if self.pass_query_string:
            return self.request.META['QUERY_STRING']

        return ''

    def _verify_config(self):
        assert self.base_url, "base_url must be set to generate a proxy url"

        # ignored_downstream_headers and ignored_request_headers must be
        # iterable
        iter(self.ignored_downstream_headers)
        iter(self.ignored_request_headers)

    def dispatch(self, request, *args, **kwargs):
        """Dispatch all HTTP methods to the proxy"""
        self.request = request
        self.args = args
        self.kwargs = kwargs

        self._verify_config()

        return self.proxy()

    def normalize_django_header_name(self, header):
        """unmunge header names normalized by Django"""
        # Remove HTTP_ prefix.
        new_header = header.rpartition('HTTP_')[2]
        # Camel case and replace _ with -
        new_header = '-'.join(
            x.capitalize() for x in new_header.split('_'))

        return new_header

    def filter_headers(self, header_dict, ignore_list):
        """Generate a header dict with a subset of the original headers"""
        filtered_headers = {}
        lowercased_ignore_list = map(lambda x: x.lower(), ignore_list)

        for header, value in header_dict.iteritems():
            if header.lower() not in lowercased_ignore_list:
                filtered_headers[header] = value

        return filtered_headers

    def proxy(self):
        """Return an HttpResponse built based on retrieving self.proxy_url"""
        xff = self.downstream_ip
        headers = self.filter_headers(
            self.headers, self.ignored_request_headers)
        result = request(
            method=self.request.method, url=self.proxy_url, headers=headers,
            data=self.request.body, params=self.query_string)

        response = HttpResponse(result.content, status=result.status_code)
        forwardable_headers = self.filter_headers(
            result.headers, self.ignored_downstream_headers)

        # Attach forwardable headers to response
        for header, value in forwardable_headers.iteritems():
            response[header] = value

        # Update X-Forwarded-For.
        if response.get('x-forwarded-for'):
            xff = '%s, %s' % (response['x-forwarded-for'], xff)

        response['x-forwarded-for'] = xff

        return response
