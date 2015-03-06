# Changelog

## 2.1.0
* Adds a middleware that sends an X-Forwarded-Proto header to upstream endpoints
  based on whether or not the incoming connection is https or http.
* Adds the `X-Forwarded-Proto` middleware to HttpProxy views by default.
* Resolves an issue that would cause djproxy to fail to install in python 2.6
  if django wasn't already installed.
* Adds a MANIFEST.in file so that relevant assets are bundled with dists.

## 2.0.0
* Renamed `HttpProxy.igorned_downstream_headers` to `ignored_upstream_headers`
* Added middleware proxy functionality for modifying content, headers before
  requests/responses are sent upstream or downstream.
* Moved XFF header functionality to a middleware
* Moved XFH header functionality to a middleware
* Moved reverse proxy functionality to a middleware
* Updated generate routes to support configuring middleware
* Reorganized the internal structure of the app for sanity's sake.

## 1.4.0
* Disable CSRF checks by default for proxies created with `generate_routes`

## 1.3.0
* Makes HttpProxy SSL verification configurable via the `verify_ssl` class
  variable.

## 1.2.0

* Fix X-Forwarded-For handling: The XFF header is now calculated correctly and
  sent to the proxied resource. Previously, the XFF header was being amended
  with the server's currenet IP address and it was being sent to the requesting
  client during the response phase. Now, the original request's header is
  amended with the client's IP address before it is sent upstream.
* djproxy now sends the X-Forwarded-Host header to the proxied resource

## 1.1.0

* Fix proxying of redirects. Previously, djproxy would follow redirects
  and render the content of the final destination. This was wrong. It now
  dutifully passes the redirect to the requester.
* Add ProxyPassReverse-like functionality via the reverse_urls class variable
  (which is now necessary because redirects are handled correctly).
* Adds the ability to generate proxies and url patterns for them from a
  configuration dict via the new `generate_routes` method.

## 1.0.0
* Fix file uploads

## 0.2.0
* Allow requests 2.1.0
* Allow Django 1.6 and fix tests to compensate for request factory changes

## 0.1.0
* Initial release
