from codecs import open
from setuptools import setup, find_packages

from djproxy import __author__, __doc__, __version__

install_requires = ['requests>=1.0.0', 'django>=1.11', 'six>=1.9.0']
tests_require = [
    'mock==2.0.0', 'nose==1.3.7', 'unittest2==1.1.0', 'spec==1.4.1',
    'requests>=1.0.0']

with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()

setup(
    name="djproxy",
    version=__version__,
    url='https://github.com/thomasw/djproxy',
    author=__author__,
    author_email='thomas.welfley+djproxy@gmail.com',
    description=__doc__.strip().split('\n')[0],
    long_description=readme,
    license='MIT',
    packages=find_packages(exclude=['tests', 'tests.*']),
    tests_require=tests_require,
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    test_suite='nose.collector'
)
