from django.core.urlresolvers import get_resolver
from mock import patch
from unittest2 import TestCase

from djproxy.urls import generate_routes, generate_proxy
from djproxy.views import HttpProxy


class GenerateRoutes(TestCase):
    """generate_routes returns routes that"""
    def setUp(self):
        self.resolver = get_resolver(None)

    def test_enable_proxy_prefixes_to_resolve(self):
        self.resolver.resolve('/yahoo/')

    def test_behave_correctly_when_passed_multiple_proxy_dicts(self):
        self.resolver.resolve('/google/')

    def test_enable_suffixes_of_proxy_prefixes_resolve(self):
        self.resolver.resolve('/google/kittens')

    def test_pass_proxy_url_suffixes_to_the_view_as_url_kwarg(
            self):
        self.assertEqual(
            self.resolver.resolve('/google/kittens/').kwargs,
            {'url': 'kittens/'})


class GenerateRoutesProxyViewGeneration(TestCase):
    """generate_routes build proxy views that"""
    def setUp(self):
        generate_proxy_patcher = patch('djproxy.urls.generate_proxy')

        self.generate_proxy_mock = generate_proxy_patcher.start()

        self.addCleanup(generate_proxy_patcher.stop)

        generate_routes({
            'yahoo_proxy': {
                'base_url': 'https://yahoo.com/',
                'prefix': '/yahoo/'
            },
        })

    def test_have_a_base_url_based_on_the_passed_config(self):
        self.generate_proxy_mock.assert_called_once_with(
            '/yahoo/', 'https://yahoo.com/')


class GenerateProxy(TestCase):
    def setUp(self):
        self.proxy = generate_proxy('/google/', 'http://google.com/')

    def test_yields_an_HttpProxy_CBGV(self):
        self.assertTrue(issubclass(self.proxy, HttpProxy))

    def test_sets_the_base_url_to_the_passed_value(self):
        self.assertEqual(self.proxy.base_url, 'http://google.com/')
