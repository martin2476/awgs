'''
    Contains all functions related to Pilot functionality
'''
import logging
import sqlite3
import config
import util

from tabulate import tabulate
from databaseDAO import DatabaseDAO


class Pilot:
    def __init__(self, pilot_id, name, surname, license_number, is_active):
        """
        Initialize a Pilot object.
        
        Args:
            pilot_id (int): Unique ID of the pilot.
            name (str): First name of the pilot.
            surname (str): Last name of the pilot.
            license_number (str): License number of the pilot.
            is_active (bool): Whether the pilot is active (True/False).
        """
        self.pilot_id = pilot_id
        self.name = name
        self.surname = surname
        self.license_number = license_number
        self.is_active = is_active

    def __str__(self):
        """
        Return a string representation of the Pilot object.
        """
        return f"Pilot(ID: {self.pilot_id}, Name: {self.name} {self.surname}, License: {self.license_number}, Active: {self.is_active})"

    def deactivate(self):
        """
        Mark the pilot as inactive.
        """
        self.is_active = False

    def activate(self):
        """
        Mark the pilot as active.
        """
        self.is_active = True
        



@util.log_function_call
def add_pilot(name, surname, licenseNumber):
    column_names=["Name", "Surname", "LicenseNumber","Is_Active"]
    values=(name, surname, licenseNumber,util.ActiveStatus.ACTIVE.value)

    outcome = DatabaseDAO.add_record(
    table_name="Pilot",
    column_names=column_names,
    values=values)

    # Construct records dynamically
    records = [{"Column": col, "Value": val} for col, val in zip(column_names, values)]

    if (outcome == True):
        print(tabulate(records, headers="keys", tablefmt="grid"))
    else:
        print("Record has not been saved.")

@util.log_function_call
def delete_pilot(pilotId):
    """
    Deletes or updates a pilot after conducting business checks:
    - If the pilot ID is not found, logs a message.
    - If the pilot is assigned to scheduled flights, they cannot be deleted.
    - If the pilot is assigned to landed flights, they are marked as "inactive."
    - If the pilot ID is not assigned to any flights, deletes the pilot record.

    Args:
    - pilotId (int): The pilot's ID.
    """

    try:
        # Check if the pilot exists
        pilot_records = DatabaseDAO.get_records("Pilot", f"PilotID = {pilotId}")
        if not pilot_records:
            logging.info("No pilot found with this ID.")
            return

        # Check if the pilot is assigned to any flights
        flight_pilot_records = DatabaseDAO.get_records("FlightPilots", f"PilotID = {pilotId}")
        if not flight_pilot_records:
            # Delete the pilot record directly
            DatabaseDAO.delete_record("Pilot", "PilotID = ?", (pilotId,))
            logging.info(f"Pilot with ID {pilotId} has been deleted.")
            return

        # Extract flight IDs linked to the pilot
        flight_ids = [record[0] for record in flight_pilot_records]
        flight_result = f"({','.join(map(str, flight_ids))})"

        # Define flight statuses that are considered active
        active_statuses = [
            util.FlightStatus.SCHEDULED, 
            util.FlightStatus.DEPARTED, 
            util.FlightStatus.BOARDING, 
            util.FlightStatus.DELAYED, 
            util.FlightStatus.LANDED
        ]
        status_result = f"({','.join(map(str, active_statuses))})"

        # Check if there are active flights linked to the pilot
        active_flights = DatabaseDAO.get_records(
            "FlightDetails", 
            f"WHERE FlightID IN {flight_result} AND FlightStatus IN {status_result}"
        )
        if active_flights:
            # Mark pilot as inactive instead of deleting
            DatabaseDAO.update_record(
                "Pilot", "Is_Active", util.ActiveStatus.INACTIVE, "PilotID", pilotId
            )
            logging.info(f"Pilot with ID {pilotId} has been marked as inactive.")
        else:
            # Delete the pilot record
            DatabaseDAO.delete_record("Pilot", "PilotID = ?", (pilotId,))
            logging.info(f"Pilot with ID {pilotId} has been deleted.")
    except Exception as e:
        logging.error(f"An error occurred while processing pilot ID {pilotId}: {e}")

@util.log_function_call    
def amend_pilot(pilotId, name=None, surname=None,licenseNumber=None,isActive=None):
    """
    Update a pilot details

    Args:
    - pilotId (int): The pilot's ID.
    - name (str): if none, then there is no change.
    - surname (str): if none, then there is no change.
    - license_number (str): if none, then there is no change.
    - isActive (ActiveStatus): if none, then there is no change
    """
    try:
        # Build updated fields dynamically
        fields = {}
        if name:
            fields["Name"] = name
        if surname:
            fields["Surname"] = surname
        if licenseNumber:
            fields["LicenseNumber"] = licenseNumber
        if isActive:
            fields["Is_Active"] = isActive

        # Join criteria with AND keyword if any exist
        query_fields = fields if fields else None

        DatabaseDAO.update_record(
                "Pilot", query_fields, "PilotID", pilotId
            )
        logging.info(f"Pilot with ID {pilotId} has been updated.")
    except Exception as e:
        logging.error(f"An error occurred while processing pilot ID {pilotId}: {e}")

@util.log_function_call
def show_pilots():
    records = DatabaseDAO.get_records("Pilot")
    if records:
        print(tabulate(records, headers="keys", tablefmt="grid"))
    else:
        print("No records found.")

@util.log_function_call
def show_pilot_schedule(pilotId):
    query = f"SELECT Name, Surname FROM Pilot WHERE PilotID = {pilotId}"
    pilot = DatabaseDAO.execute(query)
    print(f'Pilot: {pilot[0]["Name"]} {pilot[0]["Surname"]}')

    records = DatabaseDAO.get_pilot_schedule(pilotId)
    if records:
        print(tabulate(records, headers="keys", tablefmt="grid"))
    else:
        print("No records found.")

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

    


