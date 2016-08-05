import re

from django.conf.urls import url
from six import iteritems

from djproxy.views import HttpProxy


def generate_proxy(
        prefix, base_url='', verify_ssl=True, middleware=None,
        append_middleware=None, cert=None, timeout=None):
    """Generate a ProxyClass based view that uses the passed base_url."""
    middleware = list(middleware or HttpProxy.proxy_middleware)
    middleware += list(append_middleware or [])

    return type('ProxyClass', (HttpProxy,), {
        'base_url': base_url,
        'reverse_urls': [(prefix, base_url)],
        'verify_ssl': verify_ssl,
        'proxy_middleware': middleware,
        'cert': cert,
        'timeout': timeout
    })


def generate_routes(config):
    """Generate a list of urls that map to generated proxy views.

    generate_routes({
        'test_proxy': {
            'base_url': 'https://google.com/',
            'prefix': '/test_prefix/',
            'verify_ssl': False,
            'csrf_exempt: False',
            'middleware': ['djproxy.proxy_middleware.AddXFF'],
            'append_middleware': ['djproxy.proxy_middleware.AddXFF'],
            'timeout': 3.0,
            'cert': None
        }
    })

    Required configuration keys:

    * `base_url`
    * `prefix`

    Optional configuration keys:

    * `verify_ssl`: defaults to `True`.
    * `csrf_exempt`: defaults to `True`.
    * `cert`: defaults to `None`.
    * `timeout`: defaults to `None`.
    * `middleware`: Defaults to `None`. Specifying `None` causes djproxy to use
      the default middleware set. If a list is passed, the default middleware
      list specified by the HttpProxy definition will be replaced with the
      provided list.
    * `append_middleware`: Defaults to `None`. `None` results in no changes to
      the default middleware set. If a list is specified, the list will be
      appended to the default middleware list specified in the HttpProxy
      definition or, if provided, the middleware key specificed in the config
      dict.

    Returns:

    [
        url(r'^test_prefix/', GeneratedProxy.as_view(), name='test_proxy')),
    ]

    """
    routes = []

    for name, config in iteritems(config):
        pattern = r'^%s(?P<url>.*)$' % re.escape(config['prefix'].lstrip('/'))
        proxy = generate_proxy(
            prefix=config['prefix'], base_url=config['base_url'],
            verify_ssl=config.get('verify_ssl', True),
            middleware=config.get('middleware'),
            append_middleware=config.get('append_middleware'),
            cert=config.get('cert'),
            timeout=config.get('timeout'))
        proxy_view_function = proxy.as_view()

        proxy_view_function.csrf_exempt = config.get('csrf_exempt', True)

        routes.append(url(pattern, proxy_view_function, name=name))

    return routes
