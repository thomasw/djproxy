from django.test.client import RequestFactory
from unittest2 import TestCase

from djproxy.headers import HeaderDict


class HeaderDictTests(TestCase):
    def setUp(self):
        self.headers = HeaderDict({
            'My-Fake-Header': 1,
            'X-Forwarded-For': 'Cats'
        })

    def test_filter_method_exludes_headers_in_ignore_list(self):
        self.assertEqual(
            self.headers.filter(['X-Forwarded-For']), {
                'My-Fake-Header': 1
            })


class HeaderDictFromRequestMethod(TestCase):
    """HeaderDict.from_request() generates an HttpDict that"""
    def setUp(self):
        self.request = RequestFactory().get('/')

        # Fake headers that are representative of how Django munges them when
        # it sticks them into the META dict.
        self.request.META['HTTP_Host'] = 'cnn.com'
        self.request.META['HTTP_Fake_Header'] = 'header_value'
        self.request.META['HTTP_X_Forwarded_For'] = 'ipaddr 1'
        self.request.META['HTTP_UNNORMALIZED_HEADER'] = 'header value'
        self.request.META['CONTENT_TYPE'] = 'header value'

        self.headers = HeaderDict.from_request(self.request)

    def test_contains_non_http_prefixed_headers(self):
        self.assertIn('Content-Type', self.headers)

    def test_contains_http_prefixed_headers(self):
        self.assertIn('Fake-Header', self.headers)

    def test_contains_normalized_header_names(self):
        self.assertIn('Unnormalized-Header', self.headers)

    def test_has_unmodified_header_values(self):
        self.assertEqual(self.headers['Unnormalized-Header'], 'header value')
