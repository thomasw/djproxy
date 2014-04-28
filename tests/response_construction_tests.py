from django.test.client import RequestFactory
from mock import MagicMock, Mock, call
from unittest2 import TestCase

from helpers import RequestPatchMixin, ResponsePatchMixin
from test_views import TestProxy


class ResponseConstructionTest(TestCase, RequestPatchMixin,
                               ResponsePatchMixin):
    def setUp(self):
        self.proxy = TestProxy.as_view()
        self.browser_request = RequestFactory().get('/')

        self.proxy_stub = Mock(
            content='downstream content', headers={
                'Fake-Header': '123',
                'Content-Encoding': 'gzip'
            }, status_code=200)
        self.patch_request(self.proxy_stub)
        self.patch_response(MagicMock())

        self.proxy(self.browser_request)

    def tearDown(self):
        self.stop_patching_request()
        self.stop_patching_response()


class HttpProxyContentPassThrough(ResponseConstructionTest):
    def test_creates_response_object_with_proxied_content_and_status(self):
        self.response_mock.assert_called_once_with(
            'downstream content', status=200)


class HttpProxyHeaderPassThrough(ResponseConstructionTest):
    def test_sets_downstream_headers_on_response_object(self):
        self.response_stub.__setitem__.assert_any_call('Fake-Header', '123')

    def test_doesnt_set_ignored_dowstream_headers_on_response_obj(self):
        self.assertNotIn(
            call('Content-Encoding', 'gzip'),
            self.response_stub.__setitem__.mock_calls)
