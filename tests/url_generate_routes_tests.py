from django.test.client import RequestFactory
from django.core.urlresolvers import get_resolver
from mock import ANY, Mock
from unittest2 import TestCase

from helpers import RequestPatchMixin


class GenerateRoutesTest(TestCase, RequestPatchMixin):
    """generate_routes returns multiple service proxies"""
    def setUp(self):
        resolver = get_resolver(None)
        self.proxy, _, _ = resolver.resolve('/yahoo/')

        self.fake_request = RequestFactory().get('/yahoo/')
        self.patch_request(Mock(raw='', status_code=200, headers={}))
        self.proxy(self.fake_request)

    def tearDown(self):
        self.stop_patching_request()

    def test_proxies_are_configured(self):
        """generate_routes configures proxies"""
        self.request.assert_called_once_with(
            method=ANY, url='https://yahoo.com/', data=ANY, headers=ANY,
            params=ANY)
