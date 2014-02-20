from django.conf.urls import patterns
from djproxy.views import HttpProxy


def generate_routes(config):
    routes = []
    for service_name, proxy_config in config.items():
        ProxyClass = type(
            'ProxyClass',
            (HttpProxy, ),
            {'base_url': proxy_config['base_url']}
        )
        routes.append((
            r'^%s' % proxy_config['prefix'],
            ProxyClass.as_view()
        ))
    return routes
