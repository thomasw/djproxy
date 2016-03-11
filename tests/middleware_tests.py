from django.http import HttpResponse
from django.test.client import RequestFactory
from mock import Mock
from unittest2 import TestCase
from six import iteritems

from djproxy.proxy_middleware import AddXFF, AddXFH, AddXFP, ProxyPassReverse
from djproxy.request import DownstreamRequest


class AddXFFMiddlewareTest(TestCase):
    def setUp(self):
        self.request = DownstreamRequest(RequestFactory().get('/'))
        self.middleware = AddXFF()
        self.kwargs = self.middleware.process_request(
            Mock(), self.request, headers={})

    def test_adds_an_XFF_header(self):
        self.assertEqual(
            self.kwargs['headers']['X-Forwarded-For'], '127.0.0.1')


class AddXFHMiddlewareTest(TestCase):
    def setUp(self):
        self.request = DownstreamRequest(RequestFactory().get('/'))
        self.middleware = AddXFH()
        self.kwargs = self.middleware.process_request(
            Mock(), self.request, headers={})

    def test_adds_an_XFH_header(self):
        self.assertEqual(
            self.kwargs['headers']['X-Forwarded-Host'], 'testserver')


class AddXFPMiddlewareTest(TestCase):
    def get_kwargs(self, secure):
        request = Mock()
        request.is_secure.return_value = secure
        return AddXFP().process_request(Mock(), request, headers={})

    def test_sets_XFP_header_to_https_if_request_is_secure(self):
        kwargs = self.get_kwargs(secure=True)
        self.assertEqual(
            kwargs['headers']['X-Forwarded-Proto'], 'https')

    def test_sets_XFP_header_to_http_if_request_is_not_secure(self):
        kwargs = self.get_kwargs(secure=False)
        self.assertEqual(
            kwargs['headers']['X-Forwarded-Proto'], 'http')


class ProxyPassReverseTest(TestCase):
    def setUp(self):
        self.request = DownstreamRequest(RequestFactory().get('/'))
        self.middleware = ProxyPassReverse()

        # requests' response objects act like dicts of headers, so we can
        # take a little shortcut here.
        self.upstream_response = {
            'URI': 'http://upstream.tld/go/',
            'Location': 'http://upstream.tld/go/',
            'Content-Location': 'http://upstream.tld/go/',
            'Location-Foo': 'http://upstream.tld/go/'
        }
        self.view = Mock()
        self.view.reverse_urls = [('/yay/', 'http://upstream.tld/')]

        self.response = HttpResponse()

        # By default, the response objects headers will match the upstream
        # response object's headers.
        for key, value in iteritems(self.upstream_response):
            self.response[key] = value

        self.proxy_response = self.middleware.process_response(
            proxy=self.view, request=self.request,
            upstream_response=self.upstream_response, response=self.response)

    def test_patches_URI_header(self):
        self.assertEqual(
            self.proxy_response['URI'], 'http://testserver/yay/go/')

    def test_patches_Location_header(self):
        self.assertEqual(
            self.proxy_response['Location'], 'http://testserver/yay/go/')

    def test_patches_Content_Location_header(self):
        self.assertEqual(
            self.proxy_response['Content-Location'],
            'http://testserver/yay/go/')

    def test_leaves_unrelated_headers_alone(self):
        self.assertEqual(
            self.proxy_response['Location-Foo'], 'http://upstream.tld/go/')
