from django.test.client import RequestFactory
from mock import ANY, Mock
from unittest2 import TestCase

from helpers import RequestPatchMixin
from djproxy.urls import generate_routes


class GenerateRoutesGeneratesExpectedPatterns(TestCase, RequestPatchMixin):
    """generate_routes returns the expected url patterns"""
    def setUp(self):
        self.configuration = {
            'test_proxy': {
                'base_url': 'https://google.com/',
                'prefix': 'foo/',
            }
        }
        proxies = generate_routes(self.configuration)
        self.prefix = proxies[0][0]
        self.proxy = proxies[0][1]
        self.fake_request = RequestFactory().get('/yay/')

        self.patch_request(Mock(raw='', status_code=200, headers={}))

        self.proxy(self.fake_request)

    def tearDown(self):
        self.stop_patching_request()

    def test_generate_routes_returns_expected_view_when_configured(self):
        """proxy is configured from configuration"""
        self.request.assert_called_once_with(
            method=ANY, url="https://google.com/", data=ANY, headers=ANY,
            params=ANY)
        self.assertEquals(self.prefix, '^foo/')


class GenerateRoutesGeneratesMultipleProxies(TestCase, RequestPatchMixin):
    """generate_routes returns multiple service proxies"""
    def setUp(self):
        self.configuration = {
            'service_one': {
                'base_url': 'https://yahoo.com/',
                'prefix': 'yahoo/'
            },
            'service_two': {
                'base_url': 'https://google.com/',
                'prefix': 'google/'
            }
        }
        self.proxies = generate_routes(self.configuration)
        self.fake_request = RequestFactory().get('/yay/')
        self.patch_request(Mock(raw='', status_code=200, heaeders={}))

    def tearDown(self):
        self.stop_patching_request()

    def test_expected_number_of_routes_returned(self):
        """returns multiple configured proxies"""
        self.assertEqual(len(self.proxies), 2)
