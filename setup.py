from setuptools import setup, find_packages

from djproxy import __version__, __author__

# Multiprocessing is needed to execute `python setup.py tests` without any
# errors in some installations.
try:
    import multiprocessing
    multiprocessing  # resolve unused import pep8 violation by 'using' it
except:
    pass

setup(
    name="djproxy",
    version=__version__,
    url='https://github.com/thomasw/djproxy',
    download_url='https://github.com/thomasw/djproxy/releases',
    author=__author__,
    author_email='thomas.welfley+djproxy@gmail.com',
    description='djproxy is a simple reverse proxy class-based generic view '
                'for Django apps. If your application depends on proxies '
                'provided by a web server in production, djproxy can be used '
                'to duplicate that functionality during local development.',
    packages=find_packages(),
    tests_require=[
        'mock==1.0.1', 'nose==1.3.0', 'pinocchio==0.3.1', 'pyflakes==0.7.3',
        'unittest2==0.5.1', 'requests>=1.0.0', 'django>=1.4'],
    install_requires=['requests>=1.0.0', 'django>=1.4'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries',
    ],
    test_suite='nose.collector'
)
