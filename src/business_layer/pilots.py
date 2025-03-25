'''
    Contains all functions related to Pilot functionality
'''
import logging
import sqlite3
import config
import src.databaseDAO as databaseDAO
import util

from tabulate import tabulate

@util.log_function_call
def show_pilots():
    records = databaseDAO.get_records("Pilot")
    if records:
        print(tabulate(records, headers="keys", tablefmt="grid"))
    else:
        print("No records found.")
        

@util.log_function_call
def add_pilot(name, surname, licenseNumber):
    databaseDAO.add_record(
    table_name="Pilot",
    column_names=["Name", "Surname", "LicenseNumber"],
    values=(name, surname, licenseNumber))

@util.log_function_call
def delete_pilot(pilotId):
    databaseDAO.delete_record("Pilot","pilotID = ?", (pilotId,))

@util.log_function_call    
def amend_pilot(pilotId):
    pass

@util.log_function_call
def show_pilot_schedule(pilotId):
    data = databaseDAO.get_pilot_schedule(pilotId)
    print(tabulate(data, headers="keys", tablefmt="grid"))

@util.log_function_call
def show_all_pilots_schedule():
    try:
        # Use a context manager for safe connection handling
        with sqlite3.connect(config.DATABASE_NAME) as conn:
            cursor = conn.cursor()
            query = f"SELECT PilotID, Name, Surname FROM Pilot"
            cursor.execute(query)
            rows = cursor.fetchall()
            
            # Use descriptive messages while printing
            for row in rows:
                data = get_pilot_schedule(int(row[0]))
                print(f'Pilot: {row[1]} {row[2]}')
                if not data:
                    print("This pilot has no flights.")
                else:
                    print(tabulate(data, headers="keys", tablefmt="grid"))
                print()

    except sqlite3.Error as e:
        # Log database-specific errors
        logging.error(f"Database error occurred while fetching records from Pilots: {e}")
    
    except Exception as e:
        # Handle unexpected errors
        logging.error(f"Unexpected error occurred while fetching records from Pilots: {e}")

    


