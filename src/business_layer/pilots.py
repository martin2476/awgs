'''
    Contains all functions related to Pilot functionality
'''
import logging
import sqlite3
import config
import databaseUtil
import util

from tabulate import tabulate

@util.log_function_call
def show_pilots():
    databaseUtil.show_records("Pilot")

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
def get_pilot_schedule(pilotId):
    try:
        # Use a context manager for safe connection handling
        with sqlite3.connect(config.DATABASE_NAME) as conn:
            cursor = conn.cursor()
            
            # Dynamically construct the query
            # Construct query with optional criteria
            query = f"""SELECT FlightDetails.FlightName, Origin.Name, Destination.Name, FlightDetails.ScheduledFlightDate, 
                        FlightDetails.Terminal, Airline.Name,FlightDetails.FlightStatus 
                FROM FlightPilots
                INNER JOIN FlightDetails
                ON FlightPilots.FlightID = FlightDetails.FlightID
                INNER JOIN Destination As Origin
                ON FlightDetails.DestinationID = Origin.DestinationID
                INNER JOIN Destination
                ON FlightDetails.OriginID = Destination.DestinationID
                INNER JOIN Airline
                ON FlightDetails.AirlineID = Airline.AirlineID
                WHERE FlightPilots.PilotID = {pilotId}      
                """
            cursor.execute(query)
            rows = cursor.fetchall()

            # Structure the data as a list of dictionaries
            result = []
            for row in rows:
                result.append({
                    "Flight Name": row[0],
                    "Origin": row[1],
                    "Destination": row[2],
                    "Scheduled Date": row[3],
                    "Terminal": row[4],
                    "Airline": row[5],
                    "Status": row[6]
                })

        logging.info(f"show_schedule completed successfully")
        return result
    
    except sqlite3.Error as e:
        # Log database-specific errors
        logging.error(f"Database error occurred while fetching records from FlightDetails: {e}")
    
    except Exception as e:
        # Handle unexpected errors
        logging.error(f"Unexpected error occurred while fetching records from FlightDetails: {e}")      

@util.log_function_call
def show_pilot_schedule(pilotId):
    data = get_pilot_schedule(pilotId)
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

    


