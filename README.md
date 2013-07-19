#djproxy

## Tests

To run the tests, first install the dependencies:

```
pip install django==VERSION.TO.TEST.AGAINST
pip install -r requirements.txt
```

Then use django-admin.py to execute the test suite:

```
django-admin.py test --pythonpath="./" --settings=djproxy.test_settings
```
