import re

from django.conf.urls import patterns, url

from djproxy.views import HttpProxy


def generate_proxy(prefix, base_url=''):
    """Generates a ProxyClass based view that uses the passed base_url"""
    return type('ProxyClass', (HttpProxy,), {
        'base_url': base_url,
        'reverse_urls': [(prefix, base_url)]
    })


def generate_routes(config):
    """Generates a set of patterns and proxy views based on the passed config.

    generate_routes({
        'test_proxy': {
            'base_url': 'https://google.com/',
            'prefix': '/test_prefix/'
        }
    })

    Returns

    patterns(
        '',
        url(r'^test_prefix/', GeneratedProxy.as_view(), name='test_proxy'))

    """
    routes = []

    for name, config in config.iteritems():
        pattern = r'^%s(?P<url>.*)$' % re.escape(config['prefix'].lstrip('/'))
        proxy = generate_proxy(config['prefix'], config['base_url'])

        routes.append(url(pattern, proxy.as_view(), name=name))

    return patterns('', *routes)
