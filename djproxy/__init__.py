"""
djproxy is a simple reverse proxy class-based generic view for Django apps.

If an application depends on a proxy (to get around Same Origin Policy issues
in JavaScript, perhaps), djproxy can be used to provide that functionality in
a web server agnostic way. This allows developers to keep local development
environments for proxy dependent applications fully functional without needing
to run anything other than the django development server.

djproxy is also suitable for use in production environments and has been proven
to be performant in large scale deployments. However, a web server's proxy
capabilities will be *more* performant in many cases. If one needs to use this
in production, it should be fine as long as upstream responses aren't large.
Performance can be further increased by aggressively caching upstream
responses.
"""
__author__ = 'Thomas Welfley'
__version__ = '2.3.4'
