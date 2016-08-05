DEBUG = True
TEMPLATE_DEBUG = DEBUG

SECRET_KEY = 'fake_secret'

ROOT_URLCONF = 'tests.test_urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

MIDDLEWARE_CLASSES = []

INSTALLED_APPS = (
    'djproxy',
)

STATIC_ROOT = ''
STATIC_URL = '/'

APPEND_SLASH = False
