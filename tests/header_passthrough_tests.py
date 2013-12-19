from django.test.client import RequestFactory
from mock import Mock
from unittest2 import TestCase

from helpers import RequestPatchMixin
from test_views import TestProxy


class HttpProxyHeaderPassThrough(TestCase, RequestPatchMixin):
    """HttpProxy header pass through"""
    def setUp(self):
        self.proxy = TestProxy.as_view()
        self.browser_request = RequestFactory().get('/')

        # Fake headers that are representative of how Django munges them when
        # it sticks them into the META dict.
        self.browser_request.META['HTTP_Host'] = 'cnn.com'
        self.browser_request.META['HTTP_X_Forwarded_For'] = 'ipaddr 1'
        self.browser_request.META['HTTP_UNNORMALIZED_HEADER'] = 'header value'
        self.browser_request.META['CONTENT_TYPE'] = 'header value'

        self.patch_request(Mock(headers={'Fake-Header': '123'}))

        self.proxy(self.browser_request)

        # The value of the headers kwarg that gets passed to request_methd
        self.headers = self.request.mock_calls[0][2]['headers']

    def test_passes_non_http_prefixed_headers_to_proxied_endpoint(self):
        self.assertIn('Content-Type', self.headers)

    def test_filters_disallowed_headers(self):
        self.assertNotIn('Host', self.headers)

    def test_passes_django_http_prefixed_headers_to_proxied_endpoint(self):
        self.assertIn('X-Forwarded-For', self.headers)

    def test_normalizes_header_names(self):
        self.assertIn('Unnormalized-Header', self.headers)

    def test_doesnt_modify_header_values(self):
        self.assertEqual(self.headers['X-Forwarded-For'], 'ipaddr 1')
