import re

from .util import import_string


class MiddlewareSet(object):
    def __init__(self, middleware):
        self.middleware = [import_string(x)() for x in middleware]

    def process_request(self, proxy, request, **kwargs):
        for x in self.middleware:
            if not getattr(x, 'process_request', False):
                continue

            kwargs = x.process_request(proxy, request, **kwargs)

        return kwargs

    def process_response(self, proxy, request, upstream_response, response):
        for x in self.middleware:
            if not getattr(x, 'process_response', False):
                continue

            response = x.process_response(
                proxy=proxy, request=request,
                upstream_response=upstream_response,
                response=response)

        return response


class ProxyMiddlewareTemplate(object):

    """An example proxy middleware that does nothing.

    process_request(): This is called before the proxy makes a request to
    the upstream proxied endpoint. Use this method to modify what is sent
    upstream.

    process_response(): This is called before the proxy returns the results
    to the client. Use this method to modify what is sent back downstream (to
    the user).

    """

    def process_request(self, proxy, request, **kwargs):
        """Modify the keyword arguments for requests.

        proxy - the HttpProxy instance calling this method
        request - an DownstreamRequest wrapper for the django request
        kwargs - the keyword arguments to be passed to requests.request

        Returns a modified kwargs dict that will then be passed to
        request.requests.

        """
        pass

    def process_response(self, proxy, request, upstream_response, response):
        """Modify the HttpResponse object before sending it downstream.

        proxy - the HttpProxy instance calling thid method
        request - a DownstreamRequest wrapper for the django request
        upstream_response - the response object resulting from requesting the
                            proxied endpoint
        response - the django HttpResponse object to be send downstream

        Returns a modified django HttpResponse object that is then sent to
        the end user.

        """
        pass


class AddXFF(object):

    """Add an updated X-Forwarded-For header to the upstream request."""

    def process_request(self, proxy, request, **kwargs):
        kwargs['headers']['X-Forwarded-For'] = request.x_forwarded_for

        return kwargs


class AddXFH(object):
    """Add a X-Forwarded-Host header to the upstream request."""

    def process_request(self, proxy, request, **kwargs):
        kwargs['headers']['X-Forwarded-Host'] = request.get_host()

        return kwargs


class AddXFP(object):
    """Add a X-Forwarded-Proto header to the upstream request."""

    def process_request(self, proxy, request, **kwargs):
        proto = 'https' if request.is_secure() else 'http'
        kwargs['headers']['X-Forwarded-Proto'] = proto

        return kwargs


class ProxyPassReverse(object):

    """Applies reverse url rules to location headers like ProxyPassReverse.

    If the proxies reverse urls are defined as:

    [
        ('/yay/', 'http://backend.example.com/')
    ]

    Then, this middleware will search the given response object's Location,
    Content-Location, and URI headers for '^http://backend.example.com/'
    and replace matches with current hostname + /yay/.

    This is similar to Apache's ProxyPassReverse directive.

    """

    location_headers = ['URI', 'Location', 'Content-Location']

    def process_response(self, proxy, request, upstream_response, response):
        for replacement, pattern in proxy.reverse_urls:
            pattern = r'^%s' % re.escape(pattern)
            replacement = request.build_absolute_uri(replacement)

            for loc in self.location_headers:
                if not response.has_header(loc):
                    continue

                response[loc] = re.sub(pattern, replacement, response[loc])

        return response
