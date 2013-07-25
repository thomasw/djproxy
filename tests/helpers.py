from mock import patch


class RequestPatchMixin(object):
    def patch_request(self, mock_response=None):
        """patches requests.request and sets its return_value"""
        self.request_patcher = patch('djproxy.views.request')
        self.request = self.request_patcher.start()

        self.request.return_value = mock_response

        self.mock_response = mock_response

        return self.request
