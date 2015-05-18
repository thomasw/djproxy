"""Django response object generators."""
from django.http import HttpResponse, StreamingHttpResponse


class ProxyResponse(object):

    """
    Django response generator for requests library response objects.

    Given a requests response object and a streamd flag, this class can
    generate the correct type of Django Response instance with the relevant
    data from the requests response object passed to its constructor.

    >>> from djproxy.response import ProxyResponse
    >>> import requests
    >>> r = requests.get('http://httpbin.org/stream/20', stream=True)
    >>> proxy_response = ProxyResponse(response=r, stream=True)
    >>> django_response = proxy_response.generate_django_response()
    >>> list(django_response.streaming_content)
    ['...lots..', '..of..', '..content..', '...']
    >>> type(django_response)
    <class 'django.http.response.StreamingHttpResponse'>

    """

    def __init__(self, response, stream=True):
        """Return a ProxyResponse given a requests response and stream flag."""
        self.response = response
        self.stream = stream

    @property
    def _response_class(self):
        return StreamingHttpResponse if self.stream else HttpResponse

    @property
    def _content_kwarg(self):
        return 'streaming_content' if self.stream else 'content'

    @property
    def _response_content(self):
        if self.stream:
            return self.response.iter_lines()

        return self.response.content

    @property
    def _response_kwargs(self):
        return {
            'status': self.response.status_code,
            self._content_kwarg: self._response_content
        }

    def generate_django_response(self):
        """Return an appropriate Django response object for the response."""
        return self._response_class(**self._response_kwargs)
