from django.test.client import RequestFactory
from mock import Mock
from unittest2 import TestCase

from .helpers import RequestPatchMixin
from .test_views import TestProxy


class HttpProxyHeaderPassThrough(TestCase, RequestPatchMixin):
    """HttpProxy header pass through"""
    def setUp(self):
        self.proxy = TestProxy.as_view()
        self.browser_request = RequestFactory().get('/')

        # Fake headers that are representative of how Django munges them when
        # it sticks them into the META dict.
        self.browser_request.META['HTTP_Host'] = 'cnn.com'
        self.browser_request.META['HTTP_Fake_Header'] = 'header_value'
        self.browser_request.META['HTTP_X_Forwarded_For'] = 'ipaddr 1'
        self.browser_request.META['HTTP_UNNORMALIZED_HEADER'] = 'header value'
        self.browser_request.META['CONTENT_TYPE'] = 'header value'

        self.request = self.patch_request(Mock(headers={'Fake-Header': '123'}))

        self.proxy(self.browser_request)

        # The value of the headers kwarg that gets passed to request_methd
        self.headers = self.request.mock_calls[0][2]['headers']

    def test_filters_disallowed_headers(self):
        self.assertNotIn('Host', self.headers)
