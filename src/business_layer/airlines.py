'''
    Contains all functions related to Airlines functionality
'''
import util
import logging

from tabulate import tabulate
from databaseDAO import DatabaseDAO

@util.log_function_call
def show_airlines():
    records = DatabaseDAO.get_records("Airline")
    if records:
        print(tabulate(records, headers="keys", tablefmt="grid"))
    else:
        print("No records found.")        

@util.log_function_call
def add_airline(name, iataCode, terminal):
    DatabaseDAO.add_record(
    table_name="Airline",
    column_names=["Name", "IATACode", "Terminal"],
    values=(name, iataCode, terminal))


@util.log_function_call    
def amend_airline(airlineId, name=None, iataCode=None,terminal=None,isActive=None):
    """
    Update a airline details

    Args:
    - airlineId (int): The airline's ID.
    - name (str): if none, then there is no change.
    - iataCode (str): if none, then there is no change.
    - terminal (str): if none, then there is no change.
    - isActive (ActiveStatus): if none, then there is no change
    """
    try:
        # Build updated fields dynamically
        fields = {}
        if name:
            fields["Name"] = name
        if iataCode:
            fields["IATACode"] = iataCode
        if terminal:
            fields["Terminal"] = terminal
        if isActive != None:
            fields["IsActive"] = isActive

        # Join criteria with AND keyword if any exist
        query_fields = fields if fields else None

        DatabaseDAO.update_record(
                "Airline", query_fields, "AirlineID", airlineId
            )
    except Exception as e:
        logging.error(f"An error occurred while processing airline ID {airlineId}: {e}")


@util.log_function_call
def delete_airline(airlineId):
    """
    Deletes a airline after conducting business checks:
    - If the airline ID is not found, logs a message.
    - If the airline is assigned to scheduled flights, it cannot be deleted.
    - If the airline is assigned to landed flights, it is marked as "inactive."
    - If the airline ID is not assigned to any flights, deletes the airline record.

    Args:
    - airlineId (int): The airline's ID.
    """

    try:
        # Check if the airline exists
        airline_records = DatabaseDAO.get_records("Airline", f"airlineID = {airlineId}")
        if not airline_records:
            logging.info("No airline found with this ID.")
            return

        # Check if the airline is assigned to any flights
        flight_records = DatabaseDAO.get_records("FlightDetails", f"AirlineId = {airlineId}")
        if not flight_records:
            # Delete the airline record directly
            DatabaseDAO.delete_record("Airline", "AirlineID = ?", (airlineId,))
            return

        # Define flight statuses that are considered active
        status_result = util.get_active_flight_statuses()

        # Check if there are active flights linked to the airline
        active_flights = DatabaseDAO.get_records(
            "FlightDetails", 
            f"AirlineId = {airlineId} AND FlightStatus IN {status_result}"
        )
        if not active_flights:
            # Mark airline as inactive instead of deleting
            DatabaseDAO.update_record(
                "Airline", "IsActive", util.ActiveStatus.INACTIVE, "AirlineId", airlineId
            )
            logging.info(f"Airline with ID {airlineId} has been marked as inactive.")
        else:
            # There are active flights linked to this plane, it cannot be deleted or marked as in-active
            logging.info(f"Airline with ID {airlineId} cannot be deleted or marked as inactive because there are active flights linked to this airline.")
    except Exception as e:
        logging.error(f"An error occurred while processing airline ID {airlineId}: {e}")