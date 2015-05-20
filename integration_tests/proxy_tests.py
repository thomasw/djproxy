import json
from urlparse import urljoin

from django.test import LiveServerTestCase


class HttpProxyingGoodRequests(LiveServerTestCase):
    def setUp(self):
        self.url = urljoin(self.live_server_url, '/httpbin/get?foo=bar')
        self.response = self.client.get(self.url)
        self.response.json_content = json.loads(self.response.content)

    def test_sends_upstream_response_status_code_downstream(self):
        self.assertEqual(self.response.status_code, 200)

    def test_sends_query_string_upstream(self):
        self.assertEqual(self.response.json_content['args']['foo'], 'bar')


class HttpProxyingBadRequests(LiveServerTestCase):
    def setUp(self):
        self.url = urljoin(self.live_server_url, '/httpbin/status/412')
        self.response = self.client.get(self.url)

    def test_sends_upstream_response_status_code_downstream(self):
        self.assertEqual(self.response.status_code, 412)
