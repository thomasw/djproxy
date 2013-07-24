# djproxy

djproxy is a class-based generic view reverse HTTP proxy for Django.

## Contributing

To run the tests, first install the dependencies:

```
pip install -r requirements.txt
```

If you'd like to test this against a version of django other than 1.5, wipe out
the 1.5 installation from `requirements.txt` by installing the desired version.

Run `nosetests` to execute the test suite.

To run a Django dev server that proxies itself, execute the following:

```bash
$ django-admin.py runserver --settings=tests.test_settings --pythonpath="./"
```

See `tests/test_settings.py` and `tests/test_urls.py` for configuration
information.
