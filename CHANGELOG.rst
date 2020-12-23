Changelog
=========

2.3.6
-----

- Declares Django 3.1 as supported versions
- Fixes a bug that changed the names of HTTP headers that contained http. For
  example, X-Http-Method was incorrectly changed to Method.

2.3.5
-----

- Declares Django 3.0 and Python 3.8 as supported versions
- Drop support for Python 2.6
- Drop support for django < 1.11

2.3.4
-----

- Make package description less than 200 characters. This seems to be breaking
  the package metadata on pypi suddenly, even though it was fine before. This
  release contains no functional changes.

2.3.3
-----
- Fixes a bug that could interfere with subclassing HttpProxy based generic
  views.

2.3.2
-----

-  Add Django 1.10.x support.
-  Add workaround for https://code.djangoproject.com/ticket/27005 but
   restrict it to Django 1.10 specifically. The issue should be fixed in
   1.10.1.

2.3.1
-----

-  Readme updates so that pypi can render it.

2.3.0
-----

-  Add a ``timeout`` configuration to HttpProxy views allowing
   configuration of how quickly HttpProxy views give up on slow upstream
   responses.
-  Add a ``cert`` configuration option to HttpProxy views.
-  Update ``generate_routes`` and ``generate_proxy`` to support new
   configuration options.
-  Documentation updates.
-  Correct a development environment issue with six: a version that was
   too low was specified in requirements.txt which caused test failures
   in certain cases.

2.2.0
-----

-  Adds python 3 support.

2.1.0
-----

-  Adds a middleware that sends an X-Forwarded-Proto header to upstream
   endpoints based on whether or not the incoming connection is https or
   http.
-  Adds the ``X-Forwarded-Proto`` middleware to HttpProxy views by
   default.
-  Resolves an issue that would cause djproxy to fail to install in
   python 2.6 if django wasn't already installed.
-  Adds a MANIFEST.in file so that relevant assets are bundled with
   dists.

2.0.0
-----

-  Renamed ``HttpProxy.igorned_downstream_headers`` to
   ``ignored_upstream_headers``
-  Added middleware proxy functionality for modifying content, headers
   before requests/responses are sent upstream or downstream.
-  Moved XFF header functionality to a middleware
-  Moved XFH header functionality to a middleware
-  Moved reverse proxy functionality to a middleware
-  Updated generate routes to support configuring middleware
-  Reorganized the internal structure of the app for sanity's sake.

1.4.0
-----

-  Disable CSRF checks by default for proxies created with
   ``generate_routes``

1.3.0
-----

-  Makes HttpProxy SSL verification configurable via the ``verify_ssl``
   class variable.

1.2.0
-----

-  Fix X-Forwarded-For handling: The XFF header is now calculated
   correctly and sent to the proxied resource. Previously, the XFF
   header was being amended with the server's currenet IP address and it
   was being sent to the requesting client during the response phase.
   Now, the original request's header is amended with the client's IP
   address before it is sent upstream.
-  djproxy now sends the X-Forwarded-Host header to the proxied resource

1.1.0
-----

-  Fix proxying of redirects. Previously, djproxy would follow redirects
   and render the content of the final destination. This was wrong. It
   now dutifully passes the redirect to the requester.
-  Add ProxyPassReverse-like functionality via the reverse\_urls class
   variable (which is now necessary because redirects are handled
   correctly).
-  Adds the ability to generate proxies and url patterns for them from a
   configuration dict via the new ``generate_routes`` method.

1.0.0
-----

-  Fix file uploads

0.2.0
-----

-  Allow requests 2.1.0
-  Allow Django 1.6 and fix tests to compensate for request factory
   changes

0.1.0
-----

-  Initial release
