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

        Return:
        - True if no errors otherwise false
        """
        return_value = False
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
                return_value = True
        
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
            return return_value

    def update_record(table_name, columns_values, condition_column, condition_value):
        """
        A generic function to update multiple columns in a table based on a condition.

        Args:
        - table_name (str): The name of the table to update.
        - columns_values (dict): A dictionary where keys are column names and values are the new values to set.
        - condition_column (str): The column to use in the WHERE clause.
        - condition_value: The value for the WHERE clause to match.

        Example Usage:
        update_record(
            "FlightDetails", 
            {"FlightStatus": "LANDED", "Gate": "C3"}, 
            "FlightID", 
            1
        )
        """
        try:
            # Construct the SET clause dynamically
            set_clause = ", ".join([f"{column} = ?" for column in columns_values.keys()])
            
            # Extract values from the dictionary and append the condition value
            values = list(columns_values.values())
            values.append(condition_value)

            # Connect to the database using a context manager
            with sqlite3.connect(config.DATABASE_NAME) as conn:
                cursor = conn.cursor()

                # Construct the SQL query dynamically
                query = f"UPDATE {table_name} SET {set_clause} WHERE {condition_column} = ?;"
                cursor.execute(query, values)

                # Commit the transaction
                conn.commit()
                logging.info(f"Record updated successfully in {table_name}: {columns_values} where {condition_column} = {condition_value}.")

        except sqlite3.IntegrityError as e:
            logging.error(f"Integrity error while updating record in {table_name}: {e}")

        except sqlite3.Error as e:
            logging.error(f"Database error occurred while updating record in {table_name}: {e}")

        except Exception as e:
            logging.error(f"Unexpected error occurred while updating record in {table_name}: {e}")

        finally:
            logging.info("update_record completed.")
    
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
    def execute(query, params=None):
        """
        A generic function

        Args:
        - query (str): the SQL query
        - params (tuple, optional): the parameters for the SQL query
        """
        try:
            # Use a context manager for safe connection handling
            with sqlite3.connect(config.DATABASE_NAME) as conn:
                cursor = conn.cursor()
                
                # Execute the query with parameters if provided
                if params:
                    cursor.execute(query, params)
                else:
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
            logging.error(f"Database error occurred while executing query: {e}")

        except Exception as e:
            # Handle unexpected errors
            logging.error(f"Unexpected error occurred while executing query: {e}")

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
                query = f"""SELECT 
                            FlightDetails.FlightID,
                            FlightDetails.FlightName,
                            Origin.Name AS Origin,
                            Dest.Name AS Destination,
                            FlightDetails.ScheduledFlightDate,
                            COALESCE(FlightDetails.Terminal, Airline.Terminal) AS Terminal, -- Use Airline.Terminal if FlightDetails.Terminal is empty
                            Airline.Name AS Airline,
                            FlightDetails.FlightStatus
                        FROM 
                            FlightDetails
                        INNER JOIN 
                            Destination AS Origin
                            ON FlightDetails.OriginID = Origin.DestinationID
                        INNER JOIN 
                            Destination AS Dest
                            ON FlightDetails.DestinationID = Dest.DestinationID
                        INNER JOIN 
                            Airline
                            ON FlightDetails.AirlineID = Airline.AirlineID;
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
    def get_all_pilots_for_flight(flightID):    
        """
        A specific function to fetch pilot records for a particular flight.

        Args:
        - flightID (INTEGER): flight's id
        """
        try:
            # Use a context manager for safe connection handling
            with sqlite3.connect(config.DATABASE_NAME) as conn:
                cursor = conn.cursor()
                
                # Query to get all the pilots linked to a flight
                query = f"""SELECT 
                            Pilot.Name, 
                            Pilot.Surname
                        FROM 
                            FlightDetails
                        INNER JOIN 
                            FlightPilots ON FlightDetails.FlightID = FlightPilots.FlightID
                        INNER JOIN 
                            Pilot ON FlightPilots.PilotID = Pilot.PilotID
                        WHERE 
                            FlightDetails.FlightID = ?;
                    """
                cursor.execute(query,(int(flightID),))
                rows = cursor.fetchall()
                column_names = [description[0] for description in cursor.description]
                
                result = [
                    {column_names[index]: value for index, value in enumerate(row)}
                    for row in rows
                ]
                
            return result

        except sqlite3.Error as e:
            # Log database-specific errors
            logging.error(f"Database error occurred while fetching records from FlightDetails: {e}")
        
        except Exception as e:
            # Handle unexpected errors
            logging.error(f"Unexpected error occurred while fetching records from FlightDetails: {e}")

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
                            COALESCE(FlightDetails.Terminal, Airline.Terminal) AS Terminal, -- Use Airline.Terminal if FlightDetails.Terminal is empty,
                            Airline.Name,FlightDetails.FlightStatus 
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
    
      