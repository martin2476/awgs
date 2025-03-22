import logging
import sqlite3
import config

def show_pilots():
    logging.info("Showing all Pilots.")    
    show_records("Pilot")

def add_pilot(name, surname, licenseNumber):
    logging.info("Adding a Pilot.")
    add_record(
    table_name="Pilot",
    column_names=["Name", "Surname", "LicenseNumber"],
    values=(name, surname, licenseNumber))


def show_airlines():
    logging.info("Showing all Airlines.")    
    show_records("Airline")

def add_airline(name, iataCode, terminal):
    logging.info("Adding an Airline.")    
    add_record(
    table_name="Airline",
    column_names=["Name", "IATACode", "Terminal"],
    values=(name, iataCode, terminal))


def show_destinations():
    logging.info("Showing all Destinations.")
    show_records("Destination")

def add_destinations(name, country, airportCode,distanceFromLondon):
    logging.info("Adding a Destination.")
    add_record(
    table_name="Destination",
    column_names=["Name", "Country", "AirportCode","DistanceFromLondon"],
    values=(name, country, airportCode,distanceFromLondon))


def show_airplanes():
    logging.info("Showing all Planes.")
    show_records("Plane")

def add_airplane(aircraftRegistrationNumber,manufacturer,model,tailNumber,capacity):
    logging.info("Adding a Plane.")
    add_record(
    table_name="Plane",
    column_names=["AircraftRegistrationNumber", "Manufacturer", "Model","TailNumber","Capacity"],
    values=(aircraftRegistrationNumber,manufacturer,model,tailNumber,capacity))


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