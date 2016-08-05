from django.test.client import RequestFactory
from mock import Mock
from unittest2 import TestCase

from .helpers import RequestPatchMixin
from .test_views import TestProxy


class ResponseConstructionTest(TestCase, RequestPatchMixin):
    def get_request(self):
        return RequestFactory().get('/')

    def setUp(self):
        self.proxy = TestProxy.as_view()
        self.browser_request = self.get_request()

        self.proxy_stub = Mock(
            content='upstream content', headers={
                'Fake-Header': '123',
                'Transfer-Encoding': 'foo'
            }, status_code=201)
        self.patch_request(self.proxy_stub)

        self.response = self.proxy(self.browser_request)


class HttpProxyContentPassThrough(ResponseConstructionTest):
    def test_creates_response_object_with_proxied_content(self):
        self.assertEqual(
            self.response.content.decode('utf-8'), 'upstream content')

    def test_creates_response_object_with_proxied_status(self):
        self.assertEqual(self.response.status_code, 201)


class HttpProxyHeaderPassThrough(ResponseConstructionTest):
    def test_sets_upstream_headers_on_response_object(self):
        self.assertEqual(self.response['Fake-Header'], '123')

    def test_doesnt_set_ignored_upstream_headers_on_response_obj(self):
        self.assertFalse(self.response.has_header('Transfer-Encoding'))


class HttpProxyEmptyContentLengthHandling(ResponseConstructionTest):
    def get_request(self):
        request = RequestFactory().get('/')
        request.META['CONTENT_LENGTH'] = ''

        return request

    def test_succeeds(self):
        self.assertEqual(self.response.status_code, 201)
