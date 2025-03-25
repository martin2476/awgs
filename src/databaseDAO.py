import logging
import sqlite3
import config
from util import log_function_call

class DatabaseDAO:
    @log_function_call
    def add_record(table_name, column_names, values):
        """
        A generic function to insert records into any table in the database.

        Args:
        - table_name (str): Name of the table to insert into.
        - column_names (list): List of column names for the insertion.
        - values (tuple): Tuple of values corresponding to the columns.

        """
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

    @log_function_call
    def delete_record(table_name, condition, params=()):
        """
        A generic function to delete a record from any SQLite table.

        Args:
        - table_name (str): The name of the table.
        - condition (str): The WHERE clause condition (e.g., "PilotID = 3").

        Example Usage:
        delete_record("Pilot", "PilotID = 3")
        """
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

    @log_function_call
    def get_records(table_name, criteria=None):
        """
        A generic function to fetch records from any specified database table with optional selection criteria.

        Args:
        - table_name (str): Name of the table to fetch records from.
        - criteria (str, optional): SQL WHERE clause for filtering records. Default is None.
        """
        try:
            # Use a context manager for safe connection handling
            with sqlite3.connect(config.DATABASE_NAME) as conn:
                cursor = conn.cursor()
                
                # Construct query with optional criteria
                if criteria:
                    query = f"SELECT * FROM {table_name} WHERE {criteria}"
                else:
                    query = f"SELECT * FROM {table_name}"
                
                cursor.execute(query)
                rows = cursor.fetchall()
                column_names = [description[0] for description in cursor.description]

                result = [
                    {column_names[index]: value for index, value in enumerate(row)}
                    for row in rows
                ]
                
            logging.info(f"show_records completed successfully for table={table_name}, criteria={criteria}")
            return result

        except sqlite3.Error as e:
            # Log database-specific errors
            logging.error(f"Database error occurred while fetching records from {table_name}: {e}")
        
        except Exception as e:
            # Handle unexpected errors
            logging.error(f"Unexpected error occurred while fetching records from {table_name}: {e}")

    @log_function_call
    def get_flights_records(table_name, criteria=None):    
        """
        A specific function to fetch flight records with optional selection criteria.

        Args:
        - table_name (str): Name of the table to fetch records from.
        - criteria (str, optional): SQL WHERE clause for filtering records. Default is None.
        """
        try:
            # Use a context manager for safe connection handling
            with sqlite3.connect(config.DATABASE_NAME) as conn:
                cursor = conn.cursor()
                
                # Construct query with optional criteria
                query = f"""SELECT FlightDetails.FlightName, Origin.Name, Destination.Name, FlightDetails.ScheduledFlightDate, 
                            FlightDetails.Terminal, Airline.Name,FlightDetails.FlightStatus 
                    FROM FlightDetails
                    INNER JOIN Destination As Origin
                    ON FlightDetails.DestinationID = Origin.DestinationID
                    INNER JOIN Destination
                    ON FlightDetails.OriginID = Destination.DestinationID
                    INNER JOIN Airline
                    ON FlightDetails.AirlineID = Airline.AirlineID           
                    """
                
                if criteria:
                    query = f"{query} WHERE {criteria}"

                cursor.execute(query)
                rows = cursor.fetchall()
                column_names = [description[0] for description in cursor.description]
                
                result = [
                    {column_names[index]: value for index, value in enumerate(row)}
                    for row in rows
                ]
                
            return result

        except sqlite3.Error as e:
            # Log database-specific errors
            logging.error(f"Database error occurred while fetching records from {table_name}: {e}")
        
        except Exception as e:
            # Handle unexpected errors
            logging.error(f"Unexpected error occurred while fetching records from {table_name}: {e}")


    @log_function_call
    def get_pilot_schedule(pilotId):
        """
        A specific function to fetch a pilot schedule.

        Args:
        - pilotId (INTEGER): pilot's id
        """        
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
    