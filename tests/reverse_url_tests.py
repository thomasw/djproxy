from django.test.client import RequestFactory
from mock import Mock
from unittest2 import TestCase

from helpers import RequestPatchMixin
from test_views import ReverseProxy


class HttpProxyReverseURLRuleProcessing(TestCase, RequestPatchMixin):
    """HttpProxy reverse URL rule processing"""
    def setUp(self):
        self.proxy = ReverseProxy.as_view()
        self.browser_request = RequestFactory().get('/')

        # Simulate a downstream response that has location headers
        self.patch_request(Mock(headers={
            'Location': 'https://google.com/foo/',
            'URI': 'https://google.com/foo/',
            'Content-Location': 'https://google.com/foo/',
            'Blurp-Location': 'https://google.com/foo/'
        }))

        self.response = self.proxy(self.browser_request)

    def test_patches_the_location_header(self):
        self.assertEqual(
            self.response['Location'], 'http://testserver/google/foo/')

    def test_patches_the_uri_header(self):
        self.assertEqual(
            self.response['Location'], 'http://testserver/google/foo/')

    def test_patches_the_content_location_header(self):
        self.assertEqual(
            self.response['Location'], 'http://testserver/google/foo/')

    def test_leaves_non_location_headers_unchanged(self):
        self.assertEqual(
            self.response['Blurp-Location'], 'https://google.com/foo/')
