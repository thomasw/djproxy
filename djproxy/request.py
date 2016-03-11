"""Utlities for making Django request objects more useful."""

from .headers import HeaderDict


class DownstreamRequest(object):
    """A Django request wrapper that provides utilities for proxies.

    Attributes that do not exist on this class are deferred to the Django
    request object used to create the instance.

    """

    def __init__(self, request):
        """Generate a DownstreamRequest object given a Django request."""
        self._request = request

    @property
    def headers(self):
        """Request headers."""
        return HeaderDict.from_request(self._request)

    @property
    def query_string(self):
        """Request query string."""
        return self._request.META['QUERY_STRING']

    @property
    def x_forwarded_for(self):
        """X-Forwarded-For header value.

        This is the amended header so that it contains the previous IP address
        in the forwarding change.

        """
        ip = self._request.META.get('REMOTE_ADDR')
        current_xff = self.headers.get('X-Forwarded-For')

        return '%s, %s' % (current_xff, ip) if current_xff else ip

    def __getattr__(self, name):
        """Proxy the Django request object for missing attributes."""
        try:
            return self.__getattribute__(name)
        except AttributeError:
            return getattr(self._request, name)
