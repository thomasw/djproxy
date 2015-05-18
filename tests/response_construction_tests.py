from django.http import HttpResponse, StreamingHttpResponse
from django.test.client import RequestFactory
from mock import ANY, MagicMock, Mock, call
from unittest2 import TestCase

from djproxy.response import ProxyResponse

from helpers import (
    generate_upstream_response_stub, RequestPatchMixin, ResponsePatchMixin)
from test_views import TestProxy


class ResponseConstructionTest(
        TestCase, RequestPatchMixin, ResponsePatchMixin):
    def setUp(self):
        self.proxy = TestProxy.as_view()
        self.browser_request = RequestFactory().get('/')

        self.proxy_stub = generate_upstream_response_stub()
        self.patch_request(self.proxy_stub)

        self.response_stub = MagicMock()
        self.patch_response(self.response_stub)

        self.proxy(self.browser_request)

    def tearDown(self):
        self.stop_patching_request()
        self.stop_patching_response()


class HttpProxyContentPassThrough(ResponseConstructionTest):
    def test_creates_response_object_with_proxied_content(self):
        self.response_mock.assert_called_once_with(
            response=self.proxy_stub, stream=ANY)


class HttpProxyHeaderPassThrough(ResponseConstructionTest):
    def test_sets_upstream_headers_on_response_object(self):
        self.response_stub.__setitem__.assert_any_call('Fake-Header', '123')

    def test_doesnt_set_ignored_upstream_headers_on_response_obj(self):
        self.assertNotIn(
            call('Content-Encoding', 'gzip'),
            self.response_stub.__setitem__.mock_calls)


class StreamingProxyResponseGeneration(TestCase):
    def setUp(self):
        self.upstream_response_stub = Mock()
        self.upstream_response_stub.iter_lines.return_value = ['some content']

        self.proxy_response = ProxyResponse(
            response=self.upstream_response_stub, stream=True)
        self.django_response = self.proxy_response.generate_django_response()

    def test_generates_a_streaming_django_response(self):
        self.assertIsInstance(self.django_response, StreamingHttpResponse)

    def test_appropriately_passes_streaming_content_to_django_response(self):
        self.assertEqual(
            [x for x in self.django_response.streaming_content],
            self.upstream_response_stub.iter_lines())

    def test_passes_status_code_to_django_response(self):
        self.assertEqual(
            self.django_response.status_code,
            self.upstream_response_stub.status_code
        )


class NonStreamingProxyResponseGeneration(TestCase):
    def setUp(self):
        self.upstream_response_stub = Mock(content='some content')

        self.proxy_response = ProxyResponse(
            response=self.upstream_response_stub, stream=False)
        self.django_response = self.proxy_response.generate_django_response()

    def test_generates_a_normal_django_response(self):
        self.assertIsInstance(self.django_response, HttpResponse)

    def test_appropriately_passes_content_to_django_response(self):
        self.assertEqual(
            self.django_response.content, self.upstream_response_stub.content)

    def test_passes_status_code_to_django_response(self):
        self.assertEqual(
            self.django_response.status_code,
            self.upstream_response_stub.status_code
        )
