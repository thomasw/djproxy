from django.conf.urls import patterns, url

from djproxy.views import HttpProxy


def generate_routes(config):
    routes = ()
    for service_name, proxy_config in config.items():
        base_url = proxy_config['base_url']
        prefix = proxy_config['prefix']

        ProxyClass = type('ProxyClass', (HttpProxy,), {'base_url': base_url})

        routes += url(r'^%s' % prefix.lstrip('/'), ProxyClass.as_view()),

    return patterns('', *routes)
