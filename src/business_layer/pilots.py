'''
    Contains all functions related to Pilot functionality
'''
import logging
import sqlite3
import config
import util

from tabulate import tabulate
from databaseDAO import DatabaseDAO


@util.log_function_call
def show_pilots():
    records = DatabaseDAO.get_records("Pilot")
    if records:
        print(tabulate(records, headers="keys", tablefmt="grid"))
    else:
        print("No records found.")
        

@util.log_function_call
def add_pilot(name, surname, licenseNumber):
    DatabaseDAO.add_record(
    table_name="Pilot",
    column_names=["Name", "Surname", "LicenseNumber"],
    values=(name, surname, licenseNumber))

@util.log_function_call
def delete_pilot(pilotId):
    """
    This function delete a pilot after conducting a number of business checks
    - If the pilot id is not found, then nothing to do.
    - If the pilot is assigned to scheduled flights then the pilot cannot be delete
    - If the pilot is assigned to landed flights then the pilot is marked as "non active"
    - If the pilot id is not assigned to any flights, then it is deleted.

    Args:
    - pilotId (str): NameThe pilot's id.
    """    
    records = DatabaseDAO.get_records("Pilot",f"PilotID={pilotId}")
    if records == None:
        print("There is no pilot with this id.")
    else:
        records = DatabaseDAO.get_records("FlightPilots",f"PilotID={pilotId}")
        if records == None:
            DatabaseDAO.delete_record("Pilot","pilotID = ?", (pilotId))
        else:
            #Check if the flights linked to this pilot as active
            flightIDs = [record[0] for record in records]
            flightResult = f"({','.join(map(str, flightIDs))})"

            # we don't care about cancelled filghts
            flightStatusValues = [util.FlightStatus.SCHEDULED,util.FlightStatus.DEPARTED,util.FlightStatus.BOARDING,util.FlightStatus.DELAYED,util.FlightStatus.LANDED]
            statusResult = f"({','.join(map(str, flightStatusValues))})"

            records = DatabaseDAO.get_records("FlightDetails",f"WHERE FlightID in {flightResult} AND FlightStatus IN  {statusResult}")
            if records == None:
                DatabaseDAO.delete_record("Pilot","pilotID = ?", (pilotId))
            else:
                DatabaseDAO.update_record("Pilot","Is_Active",util.ActiveStatus.INACTIVE,"PilotId",pilotId)
        

@util.log_function_call    
def amend_pilot(pilotId):
    pass

@util.log_function_call
def show_pilot_schedule(pilotId):
    data = DatabaseDAO.get_pilot_schedule(pilotId)
    print(tabulate(data, headers="keys", tablefmt="grid"))

@util.log_function_call
def show_all_pilots_schedule():
    """
    A specific function which shows the schedlue for all pilots. This functions iterates through the list of pilots 
    and calls the get_pilot_schedule

    """     
    try:
        # Use a context manager for safe connection handling
        with sqlite3.connect(config.DATABASE_NAME) as conn:
            cursor = conn.cursor()
            query = f"SELECT PilotID, Name, Surname FROM Pilot"
            cursor.execute(query)
            rows = cursor.fetchall()
            
            # Use descriptive messages while printing
            for row in rows:
                data = DatabaseDAO.get_pilot_schedule(int(row[0]))
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

    


