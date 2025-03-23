import os
import sys
import pytest

print(sys.path)

import src.setupdatabase as db

# Called before  any tests are run
@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    db.cleanup_database()
    db.setup_database()


# Called after all tests have run
@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    print(f"Test session finished with exit status: {exitstatus}")    

