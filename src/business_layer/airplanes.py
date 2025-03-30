'''
    Contains all functions related to Airplanes functionality
'''
import util
import logging

from tabulate import tabulate
from databaseDAO import DatabaseDAO


@util.log_function_call
def show_airplanes():
    records = DatabaseDAO.get_records("Plane")
    if records:
        print(tabulate(records, headers="keys", tablefmt="grid"))
    else:
        print("No records found.")

@util.log_function_call
def add_airplane(aircraftRegistrationNumber,manufacturer,model,tailNumber,capacity):
    DatabaseDAO.add_record(
    table_name="Plane",
    column_names=["AircraftRegistrationNumber", "Manufacturer", "Model","TailNumber","Capacity"],
    values=(aircraftRegistrationNumber,manufacturer,model,tailNumber,capacity))


@util.log_function_call    
def amend_airplane(airplaneId, aircraftRegistrationNumber=None, manufacturer=None,model=None,tailNumber=None,capacity=None,isActive=None):
    """
    Update a airplane details

    Args:
    - airplaneId (int): The airplane's ID.
    - aircraftRegistrationNumber (str): if none, then there is no change.
    - manufacturer (str): if none, then there is no change.
    - model (str): if none, then there is no change.
    - tailNumber (int): if none, then there is no change.    
    - capacity (int): if none, then there is no change.        
    - isActive (ActiveStatus): if none, then there is no change
    """
    try:
        # Build updated fields dynamically
        fields = {}
        if aircraftRegistrationNumber:
            fields["AircraftRegistrationNumber"] = aircraftRegistrationNumber
        if manufacturer:
            fields["Manufacturer"] = manufacturer
        if model:
            fields["Model"] = model
        if tailNumber:
            fields["TailNumber"] = tailNumber
        if capacity:
            fields["Capacity"] = capacity
        if isActive:
            fields["IsActive"] = isActive

        # Join criteria with AND keyword if any exist
        query_fields = fields if fields else None

        DatabaseDAO.update_record(
                "Airplane", query_fields, "AirplaneId", airplaneId
            )
    except Exception as e:
        logging.error(f"An error occurred while processing airplane with ID {airplaneId}: {e}")


@util.log_function_call
def delete_airplane(airplaneId):
    """
    Deletes a airplane after conducting business checks:
    - If the airplane ID is not found, logs a message.
    - If the airplane is assigned to scheduled flights, it cannot be deleted.
    - If the airplane is assigned to landed flights, it is marked as "inactive."
    - If the airplane ID is not assigned to any flights, deletes the airplane record.

    Args:
    - airplaneId (int): The airplane's ID.
    """

    try:
        # Check if the airplane exists
        airplane_records = DatabaseDAO.get_records("Airplane", f"airplaneId = {airplaneId}")
        if not airplane_records:
            logging.info("No airplane found with this ID.")
            return

        # Check if the airplane is assigned to any flights
        flight_records = DatabaseDAO.get_records("FlightDetails", f"AirplaneId = {airplaneId}")
        if not flight_records:
            # Delete the airplane record directly
            DatabaseDAO.delete_record("Airplane", "AirplaneId = ?", (airplaneId,))
            return

        # Define flight statuses that are considered active
        status_result = util.get_active_flight_statuses()

        # Check if there are active flights linked to the airplane
        active_flights = DatabaseDAO.get_records(
            "FlightDetails", 
            f"WHERE PlaneId = {airplaneId} AND FlightStatus IN {status_result}"
        )
        if not active_flights:
            # Mark airplane as inactive instead of deleting
            DatabaseDAO.update_record(
                "Airplane", "IsActive", util.ActiveStatus.INACTIVE, "AirplaneId", airplaneId
            )
            logging.info(f"Airplane with ID {airplaneId} has been marked as inactive since it is associated to an Active flight.")
        else:
            # There are active flights linked to this plane, it cannot be deleted or marked as in-active
            logging.info(f"Airplane with ID {airplaneId} cannot be deleted or marked as inactive because there are active flights linked to this airplane.")
    except Exception as e:
        logging.error(f"An error occurred while processing airplane with ID {airplaneId}: {e}")