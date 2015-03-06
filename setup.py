from setuptools import setup, find_packages
import sys

from djproxy import __author__, __doc__, __version__

# Multiprocessing is needed to execute `python setup.py tests` without any
# errors in some installations.
try:
    import multiprocessing
    multiprocessing  # resolve unused import pep8 violation by 'using' it
except ImportError:
    pass

install_requires = ['requests>=1.0.0', 'django>=1.4']
tests_require = [
    'mock==1.0.1', 'nose==1.3.0', 'unittest2==0.5.1', 'requests>=1.0.0',
    'django>=1.4']

# Django >= 1.7 is not 2.6 compatible
if sys.version_info[:2] < (2, 7):
    install_requires += ['django<1.7']
    tests_require += ['django<1.7']

setup(
    name="djproxy",
    version=__version__,
    url='https://github.com/thomasw/djproxy',
    download_url='https://github.com/thomasw/djproxy/releases',
    author=__author__,
    author_email='thomas.welfley+djproxy@gmail.com',
    description=__doc__,
    packages=find_packages(exclude=['tests', 'tests.*']),
    tests_require=tests_require,
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries',
    ],
    test_suite='nose.collector'
)
