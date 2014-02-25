# Changelog

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
