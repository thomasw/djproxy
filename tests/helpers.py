from mock import patch
from mock import patch, Mock


def generate_upstream_response_stub(**kwargs):
    """Return a requests response object mock with reasonable default attrs.

    Keyword arguments will be passed to Mock, allowing the default attributes
    to be overridden at will.

    """
    kwargs['headers'] = kwargs.get('headers', {
        'Fake-Header': '123',
        'Content-Encoding': 'gzip'
    })
    kwargs['content'] = kwargs.get('content', 'upstream content')
    kwargs['status_code'] = kwargs.get('status_code', 200)

    response = Mock(**kwargs)

    # in request response objects, response content is also accessible via
    # the method iter_lines which always returns an iterable
    response.iter_lines.return_value = [kwargs['content']]

    return response


class RequestPatchMixin(object):
    def patch_request(self, mock_proxy_response=None):
        """patches requests.request and sets its return_value"""
        self.request_patcher = patch('djproxy.views.request')
        self.request = self.request_patcher.start()

        self.request.return_value = mock_proxy_response

        self.mock_proxy_response = mock_proxy_response

        return self.request

    def stop_patching_request(self):
        self.request_patcher.stop()


class ResponsePatchMixin(object):
    def patch_response(self, stub_response):
        """patches HttpResponse and sets its return_value"""
        self.response_patcher = patch('djproxy.views.HttpResponse')
        self.response_mock = self.response_patcher.start()

        self.response_mock.return_value = stub_response
        self.response_stub = stub_response

        return self.response_mock

    def stop_patching_response(self):
        self.response_patcher.stop()
