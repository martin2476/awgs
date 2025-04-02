'''
    Contains all functions related to Destinations functionality
'''
import util
import logging

from tabulate import tabulate
from databaseDAO import DatabaseDAO

@util.log_function_call
def show_destinations():
    records = DatabaseDAO.get_records("Destination")
    if records:
        print(tabulate(records, headers="keys", tablefmt="grid"))
    else:
        print("No records found.")    

@util.log_function_call
def add_destination(name, country, airportCode,distanceFromLondon):
    DatabaseDAO.add_record(
    table_name="Destination",
    column_names=["Name", "Country", "AirportCode","DistanceFromLondon","IsActive"],
    values=(name, country, airportCode,distanceFromLondon,util.ActiveStatus.ACTIVE.value))


@util.log_function_call    
def amend_destination(destinationId, name=None, country=None,airportCode=None,distanceFromLondon=None,isActive=None):
    """
    Update a destination details

    Args:
    - destinationId (int): The destination's ID.
    - name (str): if none, then there is no change.
    - country (str): if none, then there is no change.
    - airportCode (str): if none, then there is no change.
    - distanceFromLondon (int): if none, then there is no change.    
    - isActive (ActiveStatus): if none, then there is no change
    """
    try:
        # Build updated fields dynamically
        fields = {}
        if name:
            fields["Name"] = name
        if country:
            fields["Country"] = country
        if airportCode:
            fields["AirportCode"] = airportCode
        if distanceFromLondon:
            fields["DistanceFromLondon"] = distanceFromLondon        
        if isActive != None:
            fields["IsActive"] = isActive

        # Join criteria with AND keyword if any exist
        query_fields = fields if fields else None

        DatabaseDAO.update_record(
                "Destination", query_fields, "DestinationID", destinationId
            )
    except Exception as e:
        logging.error(f"An error occurred while processing destination ID {destinationId}: {e}")


@util.log_function_call
def delete_destination(destinationId):
    """
    Deletes a destination after conducting business checks:
    - If the destination ID is not found, logs a message.
    - If the destination is assigned to scheduled flights, it cannot be deleted.
    - If the destination is assigned to landed flights, it is marked as "inactive."
    - If the destination ID is not assigned to any flights, deletes the destination record.

    Args:
    - destinationId (int): The destination's ID.
    """

    try:
        # Check if the destination exists
        destination_records = DatabaseDAO.get_records("Destination", f"destinationID = {destinationId}")
        if not destination_records:
            logging.info("No destination found with this ID.")
            return

        # Check if the destination is assigned to any flights
        flight_records = DatabaseDAO.get_records("FlightDetails", f"DestinationId = {destinationId}")
        if not flight_records:
            # Delete the destination record directly
            DatabaseDAO.delete_record("Destination", "DestinationID = ?", (destinationId,))
            return

        # Define flight statuses that are considered active
        status_result = util.get_active_flight_statuses()

        # Check if there are active flights linked to the destination
        active_flights = DatabaseDAO.get_records(
            "FlightDetails", 
            f"WHERE DestinationId = {destinationId} AND FlightStatus IN {status_result}"
        )
        if not active_flights:
            # Mark destination as inactive instead of deleting
            DatabaseDAO.update_record(
                "Destination", "IsActive", util.ActiveStatus.INACTIVE, "DestinationId", destinationId
            )
            logging.info(f"Destination with ID {destinationId} has been marked as inactive.")
        else:
            # There are active flights linked to this plane, it cannot be deleted or marked as in-active
            logging.info(f"Destination with ID {destinationId} cannot be deleted or marked as inactive because there are active flights linked to this destination.")
    except Exception as e:
        logging.error(f"An error occurred while processing destination ID {destinationId}: {e}")