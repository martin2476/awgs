'''
    Contains all functions related to Pilot functionality
'''
import util
import logging
import sqlite3
import config

from tabulate import tabulate
from util import log_function_call
from databaseDAO import DatabaseDAO


@log_function_call
def show_flights(flightName=None, flightDestination=None, flightTerminal=None, flightDate=None, flightAirline=None):
    
    # Build selection criteria dynamically
    criteria = []
    if flightName:
        criteria.append(f"FlightName = '{flightName}'")
    if flightDestination:
        criteria.append(f"DestinationID = '{flightDestination}'")
    if flightTerminal:
        criteria.append(f"Terminal = '{flightTerminal}'")
    if flightDate:
        criteria.append(f"ScheduledFlightDate = '{flightDate}'")
    if flightAirline:
        criteria.append(f"Airline = '{flightAirline}'")

    # Join criteria with AND keyword if any exist
    query_criteria = " AND ".join(criteria) if criteria else None
    
    # Fetch records with optional criteria
    data = DatabaseDAO.get_flights_records("FlightDetails", query_criteria)
    print(tabulate(data, headers="keys", tablefmt="grid"))

@log_function_call
def update_flight_status(flightId,status):
    update_flight_record("FlightDetails", "FlightStatus", status, "FlightID", flightId)

@log_function_call
def update_flight_gate(flightId,gate):
    update_flight_record("FlightDetails", "FlightStatus", gate, "FlightID", flightId)

@log_function_call
def update_flight_pilot(flightId,pilotId):
    try:
        # Connect to the database using a context manager
        with sqlite3.connect(config.DATABASE_NAME) as conn:
            cursor = conn.cursor()

        pilot_flight_details = []
        cursor.executemany("""
        INSERT INTO FlightPilots (FlightID, PilotID) 
        VALUES (?, ?);
    """, pilot_flight_details)
        
    except sqlite3.IntegrityError as e:
        logging.error(f"Integrity error while updating record in FlightPilots: {e}")
    
    except sqlite3.Error as e:
        logging.error(f"Database error occurred while updating record in FlightPilots: {e}")
    
    except Exception as e:
        logging.error(f"Unexpected error occurred while updating record in FlightPilots: {e}")
    
    finally:
        logging.info("update_record completed.")

@log_function_call
def update_flight_record(table_name, column_name, value, condition_column, condition_value):
    """
    A generic function to update a specific column in a table based on a condition.

    Args:
    - table_name (str): The name of the table to update.
    - column_name (str): The column to update.
    - value: The new value to set (can be a string, integer, etc.).
    - condition_column (str): The column to use in the WHERE clause.
    - condition_value: The value for the WHERE clause to match.

    Example Usage:
    update_record("FlightDetails", "FlightStatus", "LANDED", "FlightID", 1)
    """
    try:
        # Connect to the database using a context manager
        with sqlite3.connect(config.DATABASE_NAME) as conn:
            cursor = conn.cursor()
            
            # Construct the SQL query dynamically
            query = f"UPDATE {table_name} SET {column_name} = ? WHERE {condition_column} = ?;"
            cursor.execute(query, (value, condition_value))
            
            # Commit the transaction
            conn.commit()
            logging.info(f"Record updated successfully in {table_name}: {column_name} set to {value} where {condition_column} = {condition_value}.")
    
    except sqlite3.IntegrityError as e:
        logging.error(f"Integrity error while updating record in {table_name}: {e}")
    
    except sqlite3.Error as e:
        logging.error(f"Database error occurred while updating record in {table_name}: {e}")
    
    except Exception as e:
        logging.error(f"Unexpected error occurred while updating record in {table_name}: {e}")
    
    finally:
        logging.info("update_flight_record completed.")

@util.log_function_call
def delete_flight(flightId):
    """
    Deletes a flight after conducting business checks:
    - If the flight is marked as cancelled then it can be deleted.

    Args:
    - flightId (int): The flight's ID.
    """

    try:
        # Check if the flight exists
        flight_records = DatabaseDAO.get_records("Flight", f"flightID = {flightId}")
        if not flight_records:
            logging.info("No flight found with this ID.")
            return
        
        # Build selection criteria dynamically
        criteria = []
        criteria.append(f"IsActive = '{util.FlightStatus.CANCELLED.value}'")
        criteria.append(f"FlightId = '{flightId}'")

        # Join criteria with AND keyword if any exist
        query_criteria = " AND ".join(criteria) if criteria else None
        
        # Check if the flight is cancelled
        flight_records = DatabaseDAO.get_flights_records("FlightDetails", query_criteria)
        if flight_records:
            # Delete the airline record directly
            DatabaseDAO.delete_record("Flight", "flightID = ?", (flightId,))
            return
        else:
            # There are active flights linked to this plane, it cannot be deleted or marked as in-active
            logging.info(f"Flight with ID {flightId} cannot be deleted as the flight is not cancelled.")
    except Exception as e:
        logging.error(f"An error occurred while processing flight ID {flightId}: {e}")