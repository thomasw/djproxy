from codecs import open
import multiprocessing  # noqa `python setup.py test` fix for python 2.6
from setuptools import setup, find_packages
import sys

from djproxy import __author__, __doc__, __version__

install_requires = ['requests>=1.0.0', 'django>=1.4', 'six>=1.9.0']
tests_require = [
    'mock==1.3.0', 'nose==1.3.7', 'unittest2==1.1.0', 'spec==1.3.1',
    'requests>=1.0.0']

# Django >= 1.7 is not 2.6 compatible
if sys.version_info[:2] < (2, 7):
    install_requires += ['django<1.7']

with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()

setup(
    name="djproxy",
    version=__version__,
    url='https://github.com/thomasw/djproxy',
    author=__author__,
    author_email='thomas.welfley+djproxy@gmail.com',
    description=__doc__,
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
        'Framework :: Django :: 1.4',
        'Framework :: Django :: 1.5',
        'Framework :: Django :: 1.6',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    test_suite='nose.collector'
)
