"""Generate proxy CBGVs and URL patterns for them based on config dicts."""
import re

from django.conf.urls import patterns, url

from djproxy.views import HttpProxy


def generate_proxy(
        prefix, base_url, verify_ssl=True, middleware=None,
        append_middleware=None, stream=True, **kwargs):
    """Generate an HttpProxy based vie and set the passed params as attrs."""
    middleware = list(middleware or HttpProxy.proxy_middleware)
    middleware += list(append_middleware or [])

    return type('ProxyClass', (HttpProxy,), {
        'base_url': base_url,
        'reverse_urls': [(prefix, base_url)],
        'verify_ssl': verify_ssl,
        'proxy_middleware': middleware,
        'stream': stream,
    })


def generate_routes(config):
    """Generate a set of patterns and proxy views based on the passed config.

    generate_routes({
        'test_proxy': {
            'base_url': 'https://google.com/',
            'prefix': '/test_prefix/',
            'verify_ssl': False,
            'csrf_exempt: False',
            'middleware': ['djproxy.proxy_middleware.AddXFF'],
            'append_middleware': ['djproxy.proxy_middleware.AddXFF'],
            'stream': True
        }
    })

    `base_url` and `prefix` are required. All other configuration values are
    optional.

    Default values:

    verify_ssl - True
    csrf_exempt - True
    stream - True
    middleware - HttpProxy default middleware
    append_middleware - [] (used to add additional middleware to the default)

    Returns

    patterns(
        '',
        url(r'^test_prefix/', GeneratedProxy.as_view(), name='test_proxy'))

    """
    routes = []

    for name, proxy_config in config.iteritems():
        prefix = proxy_config['prefix'].lstrip('/')
        pattern = r'^%s(?P<url>.*)$' % re.escape(prefix)
        proxy = generate_proxy(**proxy_config)

        proxy_view_function = proxy.as_view()

        proxy_view_function.csrf_exempt = proxy_config.get('csrf_exempt', True)

        routes.append(url(pattern, proxy_view_function, name=name))

    return patterns('', *routes)
