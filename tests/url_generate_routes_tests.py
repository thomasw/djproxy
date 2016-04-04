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

    def test_csrf_exempt_is_set_to_true_by_default(self):
        view_func = self.resolver.resolve('/google/kittens').func
        self.assertTrue(view_func.csrf_exempt)

    def test_csrf_exempt_can_be_configured_to_false(self):
        view_func = self.resolver.resolve('/fakey/').func
        self.assertFalse(view_func.csrf_exempt)


class GenerateRoutesProxyViewGeneration(TestCase):
    """generate_routes build proxy views that"""
    def setUp(self):
        generate_proxy_patcher = patch('djproxy.urls.generate_proxy')

        self.generate_proxy_mock = generate_proxy_patcher.start()

        self.addCleanup(generate_proxy_patcher.stop)

        self.routes = generate_routes({
            'yahoo_proxy': {
                'base_url': 'https://yahoo.com/',
                'prefix': '/yahoo/',
                'verify_ssl': False,
                'middleware': ['foo'],
                'append_middleware': ['bar'],
                'cert': 'yay.pem',
                'timeout': 5.0
            },
        })

    def test_are_configured_using_the_configuration_dict(self):
        self.generate_proxy_mock.assert_called_once_with(
            prefix='/yahoo/', base_url='https://yahoo.com/', verify_ssl=False,
            middleware=['foo'], append_middleware=['bar'], cert='yay.pem',
            timeout=5.0)


class GenerateProxy(TestCase):
    def setUp(self):
        self.proxy = generate_proxy(
            '/google/', 'http://google.com/', False, ['foo'], ['bar'],
            'yay.pem', 5.0)

    def test_yields_an_HttpProxy_CBGV(self):
        self.assertTrue(issubclass(self.proxy, HttpProxy))

    def test_sets_the_base_url_to_the_passed_value(self):
        self.assertEqual(self.proxy.base_url, 'http://google.com/')

    def test_sets_the_verify_ssl_flag_to_the_passed_value(self):
        self.assertFalse(self.proxy.verify_ssl)

    def test_sets_the_proxy_middleware_list_to_the_proper_middleware(self):
        self.assertEqual(self.proxy.proxy_middleware, ['foo', 'bar'])

    def test_sets_timeout_to_the_specified_value(self):
        self.assertEqual(self.proxy.timeout, 5.0)

    def test_sets_cert_to_the_specified_value(self):
        self.assertEqual(self.proxy.cert, 'yay.pem')
