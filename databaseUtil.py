import logging
import sqlite3
import config

# Pilot section

def show_pilots():
    logging.info("Showing all Pilots.")    
    show_records("Pilot")

def show_pilot_schedule():
    logging.info("Showing Pilot schedule.")    
    show_schedule("Pilot")

def add_pilot(name, surname, licenseNumber):
    logging.info("Adding a Pilot.")
    add_record(
    table_name="Pilot",
    column_names=["Name", "Surname", "LicenseNumber"],
    values=(name, surname, licenseNumber))

def delete_pilot(pilotId):
    logging.info("Deleting a Pilot.")
    delete_record("Pilot","pilotID = ?", (pilotId,))

def amend_pilot(pilotId):
    pass

# Airline section
def show_airlines():
    logging.info("Showing all Airlines.")    
    show_records("Airline")

def add_airline(name, iataCode, terminal):
    logging.info("Adding an Airline.")    
    add_record(
    table_name="Airline",
    column_names=["Name", "IATACode", "Terminal"],
    values=(name, iataCode, terminal))

# Destination section
def show_destinations():
    logging.info("Showing all Destinations.")
    show_records("Destination")

def add_destinations(name, country, airportCode,distanceFromLondon):
    logging.info("Adding a Destination.")
    add_record(
    table_name="Destination",
    column_names=["Name", "Country", "AirportCode","DistanceFromLondon"],
    values=(name, country, airportCode,distanceFromLondon))

# Airplane section
def show_airplanes():
    logging.info("Showing all Planes.")
    show_records("Plane")

def add_airplane(aircraftRegistrationNumber,manufacturer,model,tailNumber,capacity):
    logging.info("Adding a Plane.")
    add_record(
    table_name="Plane",
    column_names=["AircraftRegistrationNumber", "Manufacturer", "Model","TailNumber","Capacity"],
    values=(aircraftRegistrationNumber,manufacturer,model,tailNumber,capacity))

# Generic CRUD section
def add_record(table_name, column_names, values):
    """
    A generic function to insert records into any table in the database.

    Args:
    - table_name (str): Name of the table to insert into.
    - column_names (list): List of column names for the insertion.
    - values (tuple): Tuple of values corresponding to the columns.

    """
    logging.info(f"add_record started for table={table_name} with values={values}")
    
    try:
        # Connect to the database using a context manager
        with sqlite3.connect(config.DATABASE_NAME) as conn:
            cursor = conn.cursor()
            
            # Dynamically construct the query
            columns = ", ".join(column_names)
            placeholders = ", ".join(["?"] * len(column_names))
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders});"
            
            # Execute the query
            cursor.execute(query, values)
            
            # Commit the transaction
            conn.commit()
            logging.info(f"Record added successfully to {table_name}: {values}")
    
    except sqlite3.IntegrityError as e:
        # Handle specific SQLite exceptions
        logging.error(f"Integrity error while adding record to {table_name}: {e}")
    
    except sqlite3.Error as e:
        # Log general database errors
        logging.error(f"Database error occurred while adding record to {table_name}: {e}")
    
    except Exception as e:
        # Handle unexpected errors
        logging.error(f"Unexpected error occurred while adding record to {table_name}: {e}")
    
    finally:
        logging.info(f"add_record completed for table={table_name}")

def delete_record(table_name, condition, params=()):
    """
    A generic function to delete a record from any SQLite table.

    Args:
    - table_name (str): The name of the table.
    - condition (str): The WHERE clause condition (e.g., "PilotID = 3").

    Example Usage:
    delete_record("Pilot", "PilotID = 3")
    """
    logging.info(f"delete_record started for table={table_name} with condition={condition}")

    try:
        # Use a context manager to safely handle the connection
        with sqlite3.connect(config.DATABASE_NAME) as conn:
            cursor = conn.cursor()

            # Construct the SQL query dynamically
            query = f"DELETE FROM {table_name} WHERE {condition};"
            cursor.execute(query, params)

            # Commit the transaction
            conn.commit()
            logging.info(f"Record deleted successfully from {table_name} where {condition}")

    except sqlite3.Error as e:
        # Log the database error if it occurs
        logging.error(f"Database error while deleting record from {table_name}: {e}")

    except Exception as e:
        # Log unexpected errors
        logging.error(f"Unexpected error occurred while deleting record: {e}")

    finally:
        logging.info("delete_record completed.")


def show_records(table_name):
    """
    A generic function to fetch and display records from any specified database table.

    Args:
    - table_name (str): Name of the table to fetch records from.
    """
    logging.info(f"show_records started for table={table_name}")
    
    try:
        # Use a context manager for safe connection handling
        with sqlite3.connect(config.DATABASE_NAME) as conn:
            cursor = conn.cursor()
            
            # Dynamically construct the query
            query = f"SELECT * FROM {table_name}"
            cursor.execute(query)
            rows = cursor.fetchall()
            
            # Use descriptive messages while printing
            for row in rows:
                print(f"{table_name} Record: {row}")
                
        logging.info(f"show_records completed successfully for table={table_name}")
    
    except sqlite3.Error as e:
        # Log database-specific errors
        logging.error(f"Database error occurred while fetching records from {table_name}: {e}")
    
    except Exception as e:
        # Handle unexpected errors
        logging.error(f"Unexpected error occurred while fetching records from {table_name}: {e}")


def show_schedule(pilotId):
    logging.info(f"show_schedule started")
    
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