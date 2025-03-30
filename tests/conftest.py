import pytest
import logging

import src.setupdatabase as db

logging.basicConfig(
    level=logging.WARNING,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s"  # Customize log message format
    )

# Called before  any tests are run
@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    db.cleanup_database()
    db.setup_database()


# Called after all tests have run
@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    print(f"Test session finished with exit status: {exitstatus}")    

