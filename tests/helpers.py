from mock import patch


class RequestPatchMixin(object):
    def patch_request(self, mock_proxy_response=None):
        """patches requests.request and sets its return_value"""
        request_patcher = patch('djproxy.views.request')
        request = request_patcher.start()
        request.return_value = mock_proxy_response

        self.addCleanup(request_patcher.stop)

        return request
