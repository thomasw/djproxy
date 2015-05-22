import json
from urlparse import urljoin

import django
from django.test import LiveServerTestCase
from unittest2 import skipIf


@skipIf(
    django.VERSION < (1, 5), "requires Django >= 1.5 for streaming proxies")
class StreamHttpProxyingGoodRequests(LiveServerTestCase):
    def setUp(self):
        self.url = urljoin(self.live_server_url, '/httpbin-stream/get?foo=bar')
        self.response = self.client.get(self.url)
        self.response.json_content = json.loads(
            ''.join(self.response.streaming_content))

    def test_sends_upstream_response_status_code_downstream(self):
        self.assertEqual(self.response.status_code, 200)

    def test_sends_query_string_upstream(self):
        self.assertEqual(self.response.json_content['args']['foo'], 'bar')


@skipIf(
    django.VERSION < (1, 5), "requires Django >= 1.5 for streaming proxies")
class StreamHttpProxyingBadRequests(LiveServerTestCase):
    def setUp(self):
        self.url = urljoin(self.live_server_url, '/httpbin-stream/status/412')
        self.response = self.client.get(self.url)

    def test_sends_upstream_response_status_code_downstream(self):
        self.assertEqual(self.response.status_code, 412)
