from testtube.helpers import Flake8, Nosetests, Pep257


PATTERNS = (
    (r'((?!_tests\.py)(?!tube\.py).)*\.py$', [Pep257(bells=0)]),
    (r'.*\.py$', [Flake8(all_files=True)], {'fail_fast': True}),
    (r'(.*setup\.cfg$)|(.*\.coveragerc)|(.*\.py$)', [Nosetests()])
)
