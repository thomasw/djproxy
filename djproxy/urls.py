import re

from django.conf.urls import patterns, url

from djproxy.views import HttpProxy


def generate_proxy(
        prefix, base_url='', verify_ssl=True, middleware=None,
        append_middleware=None):
    """Generates a ProxyClass based view that uses the passed base_url"""
    middleware = list(middleware or HttpProxy.proxy_middleware)
    middleware += list(append_middleware or [])

    return type('ProxyClass', (HttpProxy,), {
        'base_url': base_url,
        'reverse_urls': [(prefix, base_url)],
        'verify_ssl': verify_ssl,
        'proxy_middleware': middleware
    })


def generate_routes(config):
    """Generates a set of patterns and proxy views based on the passed config.

    generate_routes({
        'test_proxy': {
            'base_url': 'https://google.com/',
            'prefix': '/test_prefix/',
            'verify_ssl': False,
            'csrf_exempt: False',
            'middleware': ['djproxy.proxy_middleware.AddXFF'],
            'append_middleware': ['djproxy.proxy_middleware.AddXFF']
        }
    })

    `verify_ssl`  and `csrf_exempt` are optional (and default to True), but
    base_url and prefix are required.

    middleware and append_middleware are also optional. If neither are present,
    the default proxy middleware set will be used. If middleware is specified,
    then the default proxy middleware list will be replaced. If
    append_middleware is specified, the list will be appended to the end of
    the middleware set. Use append_middleware if you want to add additional
    proxy behaviors without modifying the default behaviors.

    Returns

    patterns(
        '',
        url(r'^test_prefix/', GeneratedProxy.as_view(), name='test_proxy'))

    """
    routes = []

    for name, config in config.iteritems():
        pattern = r'^%s(?P<url>.*)$' % re.escape(config['prefix'].lstrip('/'))
        proxy = generate_proxy(
            prefix=config['prefix'], base_url=config['base_url'],
            verify_ssl=config.get('verify_ssl', True),
            middleware=config.get('middleware'),
            append_middleware=config.get('append_middleware'))
        proxy_view_function = proxy.as_view()

        proxy_view_function.csrf_exempt = config.get('csrf_exempt', True)

        routes.append(url(pattern, proxy_view_function, name=name))

    return patterns('', *routes)
