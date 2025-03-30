import sqlite3
import logging
import src.util as util
import src.config as config
import src.databaseDAO as du

@util.log_function_call
def test_delete_record():
    try:
        # Connect to the database using a context manager
        with sqlite3.connect(config.DATABASE_NAME) as conn:
            cursor = conn.cursor()
            
            # Execute the query
            rows = cursor.execute("SELECT COUNT(*) from Pilot where PilotID = 1")
            assert int(rows[0]) == 10

            #I know that the pilot id's are from 1 to 15
            du.delete_record("Pilot","pilotID = ?", (1,))            
    
            rows = cursor.execute("SELECT COUNT(*) from Pilot where PilotID = 1")
            assert int(rows[0]) == 2

    except sqlite3.IntegrityError as e:
        # Handle specific SQLite exceptions
        logging.error(f"Integrity error: {e}")
    
    except sqlite3.Error as e:
        # Log general database errors
        logging.error(f"Database error: {e}")
    
    except Exception as e:
        # Handle unexpected errors
        logging.error(f"Unexpected error: {e}")
       
def test_martin():
    assert 1 == 1
    