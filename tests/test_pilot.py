import sqlite3
import logging
import src.util as util
import src.config as config
import src.databaseDAO as du
import src.business_layer.pilots as pilots



@util.log_function_call
def test_delete_pilot():
    try:
        # Connect to the database using a context manager
        with sqlite3.connect(config.DATABASE_NAME) as conn:
            cursor = conn.cursor()
            
            # Execute the query
            rows = cursor.execute("SELECT COUNT(*) from Pilot where PilotID = 1")
            assert int(rows[0]) == 1

            #I know that the pilot id's are from 1 to 15
            du.delete_record("Pilot","pilotID = ?", (1,))            
    
            rows = cursor.execute("SELECT COUNT(*) from Pilot where PilotID = 1")
            assert int(rows[0]) == 0

    except sqlite3.IntegrityError as e:
        # Handle specific SQLite exceptions
        logging.error(f"Integrity error: {e}")
    
    except sqlite3.Error as e:
        # Log general database errors
        logging.error(f"Database error: {e}")
    
    except Exception as e:
        # Handle unexpected errors
        logging.error(f"Unexpected error: {e}")
       
def test_add_pilot():
    try:
        # Connect to the database using a context manager
        with sqlite3.connect(config.DATABASE_NAME) as conn:
            cursor = conn.cursor()
            
            # Confirm that a pilot with ID 16 does not exists
            rows = cursor.execute("SELECT COUNT(*) from Pilot where PilotID = 16")
            assert int(rows[0]) == 0
            
            pilots.add_pilot("Martin","Fenech","XYZ123") 
            rows = cursor.execute("SELECT COUNT(*) from Pilot where PilotID = 16")
            assert int(rows[0]) == 1
            assert str(rows[0]["Name"]) == "Marti"
            assert str(rows[0]["Surname"]) == "Fenech"
            assert str(rows[0]["LicenseNumber"]) == "XYZ123"
            assert int(rows[0]["IsActive"]) == util.ActiveStatus.INACTIVE

    except sqlite3.IntegrityError as e:
        # Handle specific SQLite exceptions
        logging.error(f"Integrity error: {e}")
    
    except sqlite3.Error as e:
        # Log general database errors
        logging.error(f"Database error: {e}")
    
    except Exception as e:
        # Handle unexpected errors
        logging.error(f"Unexpected error: {e}")
    