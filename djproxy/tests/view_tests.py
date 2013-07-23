from django.test.client import RequestFactory
from mock import ANY, Mock, patch
from unittest2 import TestCase

from djproxy.views import HttpProxy


class BadTestProxy(HttpProxy):
    pass


class GoodTestProxy(HttpProxy):
    base_url = "https://google.com/"


class RequestPatchMixin(object):
    def patch_request(self, mock_response=None):
        """patches requests.request and sets its return_value"""
        self.request_patcher = patch('djproxy.views.request')
        self.request = self.request_patcher.start()

        self.request.return_value = mock_response

        self.mock_response = mock_response

        return self.request


class HttpProxyConfigVerification(TestCase, RequestPatchMixin):
    def setUp(self):
        self.fake_request = RequestFactory().get('/')
        self.bad_proxy = BadTestProxy.as_view()
        self.good_proxy = GoodTestProxy.as_view()

        # Keep things fast by making sure that proxying doesn't actually
        # happen in these tests:
        self.patch_request(Mock(raw='', status_code=200, headers={}))

    def test_raises_an_exception_if_the_proxy_has_no_base_url(self):
        self.assertRaises(AssertionError, self.bad_proxy, self.fake_request)

    def test_passes_if_the_base_url_is_set(self):
        self.good_proxy(self.fake_request)


class HttpProxyUrlConstructionWithoutURLKwarg(TestCase, RequestPatchMixin):
    """HttpProxy proxy url construction without a URL kwarg"""
    def setUp(self):
        self.fake_request = RequestFactory().get('/yay/')
        self.proxy = GoodTestProxy.as_view()

        self.patch_request(Mock(raw='', status_code=200, headers={}))

        self.proxy(self.fake_request)

    def test_only_contains_base_url_if_no_default_url_configured(self):
        """only contains base_url"""
        self.request.assert_called_once_with(
            method=ANY, url="https://google.com/", data=ANY, headers=ANY,
            cookies=ANY, files=ANY)


class HttpProxyUrlConstructionWithURLKwarg(TestCase, RequestPatchMixin):
    """HttpProxy proxy url construction without a URL kwarg"""
    def setUp(self):
        self.fake_request = RequestFactory().get('/yay/')
        self.proxy = GoodTestProxy.as_view()

        self.patch_request(Mock(raw='', status_code=200, headers={}))

        self.proxy(self.fake_request, url="yay/")

    def test_merges_base_url_and_url_kwarg_when_both_are_present(self):
        """merges base_url and url kwarg when both are present"""
        self.request.assert_called_once_with(
            method=ANY, url="https://google.com/yay/", data=ANY, headers=ANY,
            cookies=ANY, files=ANY)

