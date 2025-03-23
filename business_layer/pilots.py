'''
    Contains all functions related to Pilot functionality
'''
import logging
import sqlite3
import config
import databaseUtil
import util

@util.log_function_call
def show_pilots():
    databaseUtil.show_records("Pilot")

@util.log_function_call
def show_pilot_schedule(pilotId):
    databaseUtil.show_schedule(pilotId)

@util.log_function_call
def add_pilot(name, surname, licenseNumber):
    databaseUtil.add_record(
    table_name="Pilot",
    column_names=["Name", "Surname", "LicenseNumber"],
    values=(name, surname, licenseNumber))

@util.log_function_call
def delete_pilot(pilotId):
    databaseUtil.delete_record("Pilot","pilotID = ?", (pilotId,))

@util.log_function_call    
def amend_pilot(pilotId):
    pass

@util.log_function_call
def show_schedule(pilotId):
    try:
        # Use a context manager for safe connection handling
        with sqlite3.connect(config.DATABASE_NAME) as conn:
            cursor = conn.cursor()
            
            # Dynamically construct the query
            query = f"SELECT * FROM FlightDetails where pilotId = {pilotId}"
            cursor.execute(query)
            rows = cursor.fetchall()
            
            # Use descriptive messages while printing
            for row in rows:
                print(f"Record: {row}")
                
        logging.info(f"show_schedule completed successfully")
    
    except sqlite3.Error as e:
        # Log database-specific errors
        logging.error(f"Database error occurred while fetching records from FlightDetails: {e}")
    
    except Exception as e:
        # Handle unexpected errors
        logging.error(f"Unexpected error occurred while fetching records from FlightDetails: {e}")      