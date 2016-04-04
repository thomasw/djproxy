from django.test.client import RequestFactory
from mock import ANY, Mock
from unittest2 import TestCase

from .helpers import RequestPatchMixin
from .test_views import (
    QuickTimeoutProxy, SpecifiedCertProxy, TestProxy, UnverifiedSSLProxy)


class HttpProxyConfigVerification(TestCase, RequestPatchMixin):
    def setUp(self):
        self.fake_request = RequestFactory().get('/')
        self.proxy = TestProxy.as_view()

        self.orig_base_url = TestProxy.base_url
        self.orig_upstream_headers = TestProxy.ignored_upstream_headers
        self.orig_request_headers = TestProxy.ignored_request_headers

        # Keep things fast by making sure that proxying doesn't actually
        # happen in these tests:
        self.patch_request(Mock(raw='', status_code=200, headers={}))

    def tearDown(self):
        TestProxy.base_url = self.orig_base_url
        TestProxy.ignored_upstream_headers = self.orig_upstream_headers
        TestProxy.ignored_request_headers = self.orig_request_headers

    def test_raises_an_exception_if_the_proxy_has_no_base_url(self):
        TestProxy.base_url = ''
        self.assertRaises(AssertionError, self.proxy, self.fake_request)

    def test_raises_an_exception_if_upstream_ignore_list_not_iterable(self):
        TestProxy.ignored_upstream_headers = None
        self.assertRaises(TypeError, self.proxy, self.fake_request)

    def test_raises_an_exception_if_request_headers_ignore_list_not_iterable(
            self):
        TestProxy.ignored_request_headers = None
        self.assertRaises(TypeError, self.proxy, self.fake_request)

    def test_passes_if_the_base_url_is_set(self):
        self.proxy(self.fake_request)


class HttpProxyUrlConstructionWithoutURLKwarg(TestCase, RequestPatchMixin):
    """HttpProxy proxy url construction without a URL kwarg"""
    def setUp(self):
        self.fake_request = RequestFactory().get('/yay/')
        self.proxy = TestProxy.as_view()

        self.request = self.patch_request(
            Mock(raw='', status_code=200, headers={}))

        self.proxy(self.fake_request)

    def test_only_contains_base_url_if_no_default_url_configured(self):
        """only contains base_url"""
        self.request.assert_called_once_with(
            method=ANY, url='https://google.com/', data=ANY, headers=ANY,
            params=ANY, allow_redirects=ANY, verify=ANY, cert=ANY, timeout=ANY)


class HttpProxyUrlConstructionWithURLKwarg(TestCase, RequestPatchMixin):
    """HttpProxy proxy url construction with a URL kwarg"""
    def setUp(self):
        self.fake_request = RequestFactory().get('/yay/')
        self.proxy = TestProxy.as_view()

        self.request = self.patch_request(
            Mock(raw='', status_code=200, headers={}))

        self.proxy(self.fake_request, url='yay/')

    def test_urljoins_base_url_and_url_kwarg(self):
        """urljoins base_url and url kwarg"""
        self.request.assert_called_once_with(
            method=ANY, url='https://google.com/yay/', data=ANY, headers=ANY,
            params=ANY, allow_redirects=ANY, verify=ANY, cert=ANY, timeout=ANY)


class HttpProxyUrlConstructionWithQueryStringPassingEnabled(
        TestCase, RequestPatchMixin):
    """HttpProxy URL construction with query string passing enabled"""
    def setUp(self):
        self.fake_request = RequestFactory().get('/yay/?yay=foo,bar')
        self.proxy = TestProxy.as_view()

        self.request = self.patch_request(
            Mock(raw='', status_code=200, headers={}))

        self.proxy(self.fake_request, url='yay/')

    def test_sends_query_string_to_proxied_endpoint(self):
        self.request.assert_called_once_with(
            method=ANY, url=ANY, data=ANY, headers=ANY, params='yay=foo,bar',
            allow_redirects=ANY, verify=ANY, cert=ANY, timeout=ANY)


class HttpProxyUrlConstructionWithoutQueryStringPassingEnabled(
        TestCase, RequestPatchMixin):
    """HttpProxy URL construction without query string passing enabled"""
    def setUp(self):
        TestProxy.pass_query_string = False
        self.fake_request = RequestFactory().get('/yay/?yay=foo,bar')
        self.proxy = TestProxy.as_view()

        self.request = self.patch_request(
            Mock(raw='', status_code=200, headers={}))

        self.proxy(self.fake_request, url='yay/')

    def tearDown(self):
        TestProxy.pass_query_string = True

    def test_doesnt_sends_query_string_to_proxied_endpoint(self):
        self.request.assert_called_once_with(
            method=ANY, url=ANY, data=ANY, headers=ANY, params='',
            allow_redirects=ANY, verify=ANY, cert=ANY, timeout=ANY)


class HttpProxyFetchingWithVerifySSL(TestCase, RequestPatchMixin):
    """HttpProxy content fetching with verify_ssl enabled"""
    def setUp(self):
        self.fake_request = RequestFactory().get('/')
        self.proxy = TestProxy.as_view()

        self.request = self.patch_request(
            Mock(raw='', status_code=200, headers={}))

        self.proxy(self.fake_request, url='yay/')

    def test_tells_requests_to_verify_the_SSL_certs(self):
        self.request.assert_called_once_with(
            method=ANY, url=ANY, data=ANY, headers=ANY, params=ANY,
            allow_redirects=ANY, verify=True, cert=ANY, timeout=ANY)


class HttpProxyFetchingWithoutVerifySSL(TestCase, RequestPatchMixin):
    """HttpProxy content fetching with verify_ssl disabled"""
    def setUp(self):
        self.fake_request = RequestFactory().get('/')
        self.proxy = UnverifiedSSLProxy.as_view()

        self.request = self.patch_request(
            Mock(raw='', status_code=200, headers={}))

        self.proxy(self.fake_request, url='yay/')

    def test_tells_requests_not_to_verify_the_ssl_certs(self):
        self.request.assert_called_once_with(
            method=ANY, url=ANY, data=ANY, headers=ANY, params=ANY,
            allow_redirects=ANY, verify=False, cert=ANY, timeout=ANY)


class HttpProxyFetchingWithCert(TestCase, RequestPatchMixin):
    """HttpProxy fetching with cert specified"""
    def setUp(self):
        self.fake_request = RequestFactory().get('/')
        self.proxy = SpecifiedCertProxy.as_view()

        self.request = self.patch_request(
            Mock(raw='', status_code=200, headers={}))

        self.proxy(self.fake_request, url='yay/')

    def test_tells_requests_to_use_specific_cert(self):
        self.request.assert_called_once_with(
            method=ANY, url=ANY, data=ANY, headers=ANY, params=ANY,
            allow_redirects=ANY, verify=ANY, cert=('cert.pem', 'key.pem'),
            timeout=ANY)


class HttpProxyFetchingWithTimeoutConfigured(TestCase, RequestPatchMixin):
    """HttpProxy fetching with timeout specified"""
    def setUp(self):
        self.fake_request = RequestFactory().get('/')
        self.proxy = QuickTimeoutProxy.as_view()

        self.request = self.patch_request(
            Mock(raw='', status_code=200, headers={}))

        self.proxy(self.fake_request, url='yay/')

    def test_tells_requests_to_use_specific_timeout(self):
        self.request.assert_called_once_with(
            method=ANY, url=ANY, data=ANY, headers=ANY, params=ANY,
            allow_redirects=ANY, verify=ANY, cert=ANY,
            timeout=(0.1, 0.1))
