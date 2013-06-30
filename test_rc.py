
import os
import datetime

import rc

from nose import with_setup

def setup_func():
    try:
        os.unlink("rc.jpkl")
    except (IOError, OSError):
        pass

def teardown_func():
    pass

@with_setup(setup_func, teardown_func)
def test_add():
    rc.add("asdf")

    db = rc._load()
    assert db['tasks'][0]['name'] == 'asdf'

@with_setup(setup_func, teardown_func)
def test_complete():
    rc.add("asdf")
    result = rc.complete("asdf")

    # Should return None if successful.
    assert not result

    db = rc._load()
    assert db['tasks'][0]['name'] == 'asdf'
    assert db['tasks'][0]['next_date'] >= datetime.datetime.today()

@with_setup(setup_func, teardown_func)
def test_checklist():
    rc.add("asdf")
    rc.complete("asdf")
    result = rc.checklist()

    assert result == ["[ ] asdf (in 6 days.)",]
