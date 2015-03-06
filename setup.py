from setuptools import setup, find_packages

from djproxy import __author__, __doc__, __version__

# Multiprocessing is needed to execute `python setup.py tests` without any
# errors in some installations.
try:
    import multiprocessing
    multiprocessing  # resolve unused import pep8 violation by 'using' it
except ImportError:
    pass

setup(
    name="djproxy",
    version=__version__,
    url='https://github.com/thomasw/djproxy',
    download_url='https://github.com/thomasw/djproxy/releases',
    author=__author__,
    author_email='thomas.welfley+djproxy@gmail.com',
    packages=find_packages(),
    tests_require=[
        'mock==1.0.1', 'nose==1.3.0', 'pinocchio==0.3.1', 'pyflakes==0.7.3',
        'unittest2==0.5.1', 'requests>=1.0.0', 'django>=1.4'],
    install_requires=['requests>=1.0.0', 'django>=1.4'],
    description=__doc__,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries',
    ],
    test_suite='nose.collector'
)
