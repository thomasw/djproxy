# djproxy

djproxy is class-based generic view HTTP proxy for Django.

## Contributing

To run the tests, first install the dependencies:

```
pip install -r requirements.txt
```

If you'd like to test this against a version of django other than 1.5, wipe out
the 1.5 installation from `requirements.txt` by installing the desired version.

Use django-admin.py to execute the test suite:

```
django-admin.py test --pythonpath="./" --settings=tests.test_settings
```
