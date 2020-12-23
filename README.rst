djproxy
=======

|Build Status| |Coverage Status| |Latest Version| |PyPI - Python Version| |PyPI - Downloads|

.. |Build Status| image:: https://img.shields.io/travis/com/thomasw/djproxy.svg
   :target: https://travis-ci.com/thomasw/djproxy
.. |Coverage Status| image:: https://img.shields.io/coveralls/thomasw/djproxy.svg
   :target: https://coveralls.io/r/thomasw/djproxy
.. |Latest Version| image:: https://img.shields.io/pypi/v/djproxy.svg
   :target: https://pypi.python.org/pypi/djproxy/
.. |PyPI - Python Version| image:: https://img.shields.io/pypi/pyversions/djproxy.svg
   :target: https://pypi.python.org/pypi/djproxy/
.. |PyPI - Downloads| image:: https://img.shields.io/pypi/dm/djproxy.svg
   :target: https://pypi.python.org/pypi/djproxy/

Why?
----

If an application depends on a proxy (to get around Same Origin Policy
issues in JavaScript, perhaps), djproxy can be used to provide that
functionality in a web server agnostic way. This allows developers to
keep local development environments for proxy dependent applications
fully functional without needing to run anything other than the django
development server.

djproxy is also suitable for use in production environments and has been
proven to be performant in large scale deployments. However, a web
server's proxy capabilities will be *more* performant in many cases. If
one needs to use this in production, it should be fine as long as
upstream responses aren't large. Performance can be further increased by
aggressively caching upstream responses.

Note that djproxy doesn't currently support websockets.

Installation
------------

::

    pip install djproxy

djproxy requires requests >= 1.0.0, django >= 1.11 and python >= 2.7. The goal
is to maintain compatibility with all versions of `Django that are still
officially supported
<https://www.djangoproject.com/download/#supported-versions>`_. However, djproxy
may still work with older versions.

If you encounter issues using djproxy with a supported version of django, please
report it.

Usage
-----

Start by defining a new proxy:

.. code:: python

    from djproxy.views import HttpProxy

    class LocalProxy(HttpProxy):
        base_url = 'https://google.com/'

Add a url pattern that points at the proxy view. The ``url`` kwarg will
be urljoined with base\_url:

.. code:: python

    urlpatterns = [
        url(r'^local_proxy/(?P<url>.*)$', LocalProxy.as_view(), name='proxy')
    ]

``/local_proxy/some/content`` will now proxy
``https://google.com/some/content/``.

Additional examples can be found here:
`views <https://github.com/thomasw/djproxy/blob/master/tests/test_views.py>`_,
`urls <https://github.com/thomasw/djproxy/blob/master/tests/test_urls.py>`_.

HttpProxy configuration:
~~~~~~~~~~~~~~~~~~~~~~~~

``HttpProxy`` view's behavior can be further customized by overriding
the following class attributes.

-  ``base_url``: The proxy url is formed by
   ``urlparse.urljoin(base_url, url_kwarg)``
-  ``ignored_upstream_headers``: A list of headers that shouldn't be
   forwarded to the browser from the proxied endpoint.
-  ``ignored_request_headers``: A list of headers that shouldn't be
   forwarded to the proxied endpoint from the browser.
-  ``proxy_middleware``: A list of proxy middleware to apply to request
   and response data.
-  ``pass_query_string``: A boolean indicating whether the query string
   should be sent to the proxied endpoint.
-  ``reverse_urls``: An iterable of location header replacements to be
   made on the constructed response (similar to Apache's
   ``ProxyPassReverse`` directive).
-  ``verify_ssl``\*: This attribute corresponds to `requests' verify
   parameter <http://docs.python-requests.org/en/latest/user/advanced/?highlight=verify#ssl-cert-verification>`_.
   It may be either a boolean, which toggles SSL certificate
   verification on or off, or the path to a CA\_BUNDLE file for private
   certificates.
-  ``cert``\*: This attribute corresponds to `requests' cert
   parameter <http://docs.python-requests.org/en/latest/user/advanced/?highlight=verify#ssl-cert-verification>`_.
   If a string is specified, it will be treated as a path to an ssl
   client cert file (.pem). If a tuple is specified, it will be treated
   as a ('cert', 'key') pair.
-  ``timeout``\*: This attribute corresponds to `requests' timeout
   parameter <http://docs.python-requests.org/en/master/api/#requests.request>`_.
   It is used to specify how long to wait for the upstream server to
   send data before giving up. The value must be either a float
   representing the total timeout time in seconds, or a (connect timeout
   float, read timeout float) tuple.

\* The behavior changes that result from configuring ``verify_ssl``,
``cert``, and ``timeout`` will ultimately be dependent on the specific
version of requests that's installed. For example, in older versions of
requests, tuple values are not supported for the ``cert`` and
``timeout`` properties.

Adjusting location headers (ProxyPassReverse)
---------------------------------------------

Apache has a directive called ``ProxyPassReverse`` that makes
replacements to three location headers: ``URI``, ``Location``, and
``Content-Location``. Without this functionality, proxying an endpoint
that returns a redirect with a ``Location`` header of
``http://foo.bar/go/cats/`` would cause a downstream requestor to be
redirected away from the proxy. djproxy has a similar mechanism which is
exposed via the ``reverse_urls`` class variable. The following proxies
are equivalent:

Djproxy:

.. code:: python


    class ReverseProxy(HttpProxy):
        base_url = 'https://google.com/'
        reverse_urls = [
            ('/google/', 'https://google.com/')
        ]

    urlpatterns = patterns[
        url(r'^google/(?P<url>.*)$', ReverseProxy.as_view(), name='gproxy')
    ]

Apache:

::

    <Proxy https://google.com/*>
        Order deny,allow
        Allow from all
    </Proxy>
    ProxyPass /google/ https://google.com/
    ProxyPassReverse /google/ https://google.com/

HttpProxy dynamic configuration and route generation helper:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To specify the configuration for a set of proxies, without having to
maintain specific classes and url routes, one can use
``djproxy.helpers.generate_routes`` as follows:

In ``urls.py``, pass ``generate_routes`` a ``configuration`` dict to
configure a set of proxies:

.. code:: python

    from djproxy.urls import generate_routes

    configuration = {
        'test_proxy': {
            'base_url': 'https://google.com/',
            'prefix': '/test_prefix/',
        },
        'service_name': {
            'base_url': 'https://service.com/',
            'prefix': '/service_prefix/',
            'verify_ssl': False,
            'append_middlware': ['myapp.proxy_middleware.add_headers']
        }
    }

    urlpatterns += generate_routes(configuration)

Using the snippet above will enable a Django app to proxy
``https://google.com/X`` at ``/test_prefix/X`` and
``https://service.com/Y`` at ``/service_prefix/Y``.

These correspond to the following production Apache proxy configuration:

::

    <Proxy https://google.com/*>
        Order deny,allow
        Allow from all
    </Proxy>
    ProxyPass /test_prefix/ https://google.com/
    ProxyPassReverse /test_prefix/ https://google.com/


    <Proxy https://service.com/*>
        Order deny,allow
        Allow from all
    </Proxy>
    ProxyPass /service_prefix/ http://service.com/
    ProxyPassReverse /service_prefix/ http://service.com/

Required configuration keys:

-  ``base_url``
-  ``prefix``

Optional configuration keys:

-  ``verify_ssl``: defaults to ``True``.
-  ``csrf_exempt``: defaults to ``True``.
-  ``cert``: defaults to ``None``.
-  ``timeout``: defaults to ``None``.
-  ``middleware``: Defaults to ``None``. Specifying ``None`` causes
   djproxy to use the default middleware set. If a list is passed, the
   default middleware list specified by the HttpProxy definition will be
   replaced with the provided list.
-  ``append_middleware``: Defaults to ``None``. ``None`` results in no
   changes to the default middleware set. If a list is specified, the
   list will be appended to the default middleware list specified in the
   HttpProxy definition or, if provided, the middleware key specified in
   the config dict.

Proxy middleware
----------------

HttpProxys support custom middleware for preprocessing data from
downstream to be sent to upstream endpoints and for preprocessing
response data before it is sent back downstream. ``X-Forwarded-Host``,
``X-Forwarded-For``, ``X-Forwarded-Proto`` and the ``ProxyPassRevere``
functionality area all implemented as middleware.

HttProxy views are configured to execute particular middleware by
setting their ``proxy_middleware`` attribute. The following HttpProxy
would attach XFF and XFH headers, but not preform the ProxyPassReverse
header translation or attach an XFP header:

.. code:: python

    class ReverseProxy(HttpProxy):
        base_url = 'https://google.com/'
        reverse_urls = [
            ('/google/', 'https://google.com/')
        ]
        proxy_middleware = [
            'djproxy.proxy_middleware.AddXFF',
            'djproxy.proxy_middleware.AddXFH'
        ]

If a custom middleware is needed to modify content, headers, cookies,
etc before the content is sent upstream of if one needs to make similar
modifications before the content is sent back downstream, a custom
middleware can be written and proxy views can be configured to use it.
djproxy contains a `middleware
template <https://github.com/thomasw/djproxy/blob/master/djproxy/proxy_middleware.py#L32>`_
to make this process easier.

Terminology
-----------

It is important to understand the meaning of these terms in the context
of this project:

**upstream**: The destination that is being proxied.

**downstream**: The agent that initiated the request to djproxy.

Contributing
------------

To run the tests, first install development dependencies:

::

    pip install -r requirements.txt

To test this against a version of Django other than the latest supported
on the test environment's Python version, wipe out the
``requirements.txt`` installation by pip installing the desired version.

Run ``nosetests`` to execute the test suite.

To automatically run the test suite, flake8, and pep257 checks whenever python
files change use testtube by executing ``stir`` in the top level djproxy
directory.

To run a Django dev server that proxies itself, execute the following:

::

    django-admin.py runserver --settings=tests.test_settings --pythonpath="./"

Similarly, to run a configure Django shell, execute the following:

::

    django-admin.py shell --settings=tests.test_settings --pythonpath="./"

See ``tests/test_settings.py`` and ``tests/test_urls.py`` for
configuration information.
