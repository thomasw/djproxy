import re

# The Cookie module has been renamed to http.cookies in Python 3.0.
# We use its equivalent re_path to maintain compatibility
# with older versions of django
try:
    from http.cookies import SimpleCookie
except ImportError as exception:
    from Cookie import SimpleCookie

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


class ForwardSetCookie(object):
    """
    Handles the transmission of multiple cookies returned by a server as multiple set-cookie headers.

    Request merges the set-cookie headers into one. The default behavior is ok
    if the server returns only one cookie per http response.

    The browser will receive only one cookie.

    {
        Set-Cookie: hello=world; Expires=Wed, 21 Oct 2015 07:28:00 GMT, world=hello
    }

    instead

    {
        Set-Cookie: hello=world; Expires=Wed, 21 Oct 2015 07:28:00 GMT
        Set-Cookie: world=hello
    }

    more about this behavior

    * https://github.com/urllib3/urllib3/commit/d8013cb111644a06eb5cb9bccce174a1a996078d
    * https://stackoverflow.com/a/57131320
    * https://github.com/psf/requests/issues/3957#issuecomment-1047539652
    """
    def process_response(self, proxy, request, upstream_response, response):
        if 'set-cookie' in response:
            # The set-cookie headers are well present in the headers of urlib3 forwarded by request
            # On its own interface, request has merged those cookies in one single header
            for header, value in  upstream_response.raw.headers.items():
                if header.lower() == 'set-cookie':
                    cookies = SimpleCookie(value)
                    for key in cookies.keys():
                        cookie = cookies.get(key)
                        response.set_cookie(cookie.key,
                                            value=cookie.value,
                                            expires=cookie.get('expires'),
                                            path=cookie.get('path'),
                                            domain=cookie.get('domain'),
                                            secure=True if cookie.get('secure') else False,
                                            httponly=True if cookie.get('httponly') else False)

            # remove the default header added by request
            del response['set-cookie']

        return response


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
