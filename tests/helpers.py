from mock import patch


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
