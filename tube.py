from testtube.helpers import Flake8, Frosted, Nosetests, Pep257


PATTERNS = (
    (r'((?!test_)(?!tube\.py).)*\.py$', [Pep257(bells=0)]),
    (r'.*\.py$', [Flake8(all_files=True), Frosted(all_files=True)],
     {'fail_fast': True}),
    (r'(.*setup\.cfg$)|(.*\.coveragerc)|(.*\.py$)', [Nosetests()])
)
