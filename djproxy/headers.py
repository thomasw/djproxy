"""Utilities for handling sets of headers."""
from six import iteritems


class HeaderDict(dict):

    """A dict containing header, value pairings."""

    @staticmethod
    def _normalize_django_header_name(header):
        """Unmunge header names modified by Django."""
        # Remove HTTP_ prefix.
        new_header = header.rpartition('HTTP_')[2]
        # Camel case and replace _ with -
        new_header = '-'.join(
            x.capitalize() for x in new_header.split('_'))

        return new_header

    @classmethod
    def from_request(cls, request):
        """Generate a HeaderDict based on django request object meta data."""
        request_headers = HeaderDict()
        other_headers = ['CONTENT_TYPE', 'CONTENT_LENGTH']

        for header, value in iteritems(request.META):
            is_header = header.startswith('HTTP_') or header in other_headers
            normalized_header = cls._normalize_django_header_name(header)

            if is_header and value:
                request_headers[normalized_header] = value

        return request_headers

    def filter(self, exclude):
        """Return a HeaderSet excluding the headers in the exclude list."""
        filtered_headers = HeaderDict()
        lowercased_ignore_list = [x.lower() for x in exclude]

        for header, value in iteritems(self):
            if header.lower() not in lowercased_ignore_list:
                filtered_headers[header] = value

        return filtered_headers
