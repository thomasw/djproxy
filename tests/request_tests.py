from django.test.client import RequestFactory
from unittest2 import TestCase

from djproxy.request import DownstreamRequest


class DownstreamRequestsTest(TestCase):
    def setUp(self):
        self.request = RequestFactory().get('/foo?bar=1')
        self.request.META['HTTP_my_header'] = 'foo'
        self.downstream_request = DownstreamRequest(self.request)

    def test_has_a_valid_query_string_attribute(self):
        self.assertEqual(self.downstream_request.query_string, 'bar=1')

    def test_proxy_attributes_to_their_Django_request_isntance(self):
        self.assertEqual(
            self.request.get_host(), self.downstream_request.get_host())

    def test_x_forwarded_for_attribute_returns_requestor(self):
        self.assertEqual(
            self.downstream_request.x_forwarded_for, '127.0.0.1')

    def test_header_attribute_returns_header_set_containing_http_headers(self):
        self.assertEqual(self.downstream_request.headers['My-Header'], 'foo')


class PreviouslyForwardedDownstreamRequestsTest(TestCase):
    def setUp(self):
        self.request = RequestFactory().get('/foo?bar=1')
        self.request.META['HTTP_X_FORWARDED_FOR'] = '127.0.0.2'
        self.downstream_request = DownstreamRequest(self.request)

    def test_x_forwarded_for_attribute_appends_last_requestor(self):
        self.assertEqual(
            self.downstream_request.x_forwarded_for, '127.0.0.2, 127.0.0.1')
