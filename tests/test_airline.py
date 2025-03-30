import uuid
import sqlite3
import logging
import src.util as util
import src.config as config
import src.business_layer.airlines as airlines

@util.log_function_call
def test_delete_airline():
    try:
        # Connect to the database using a context manager
        with sqlite3.connect(config.DATABASE_NAME) as conn:
            conn.row_factory = sqlite3.Row #Allow accessing rows as dictionary
            cursor = conn.cursor()
            
            #Generate a random name to be sure there are no conflicts
            name = str(uuid.uuid4())

            cursor.execute(f"SELECT COUNT(*) from Airline where Name = ?",(name,))
            row = cursor.fetchone()
            assert row[0] == 0 # Ensure there are no airlines with this name

            #Add the airline
            cursor.execute("""
                    INSERT INTO Airline (Name, IATACode, Terminal,IsActive)
                    VALUES (?, ?, ?, ?);
                """, 
                (name, 'bla bla', 'tyr123',util.ActiveStatus.ACTIVE.value))
            conn.commit()


            #Verify that the airline was inserted
            cursor.execute(f"Select AirlineId,Name from Airline where Name = ?",(name,))
            row = cursor.fetchone()
            assert row is not None 
            assert row["Name"] == name
           
            airlineId = row["AirlineID"]
            airlines.delete_airline(airlineId) #this has its own commit
            cursor.execute(f"SELECT COUNT(*) from Airline where AirlineId = ?",(airlineId,))
            row = cursor.fetchone()
            assert row[0] == 0 #Ensure the airline does no longer exists

    except sqlite3.IntegrityError as e:
        # Handle specific SQLite exceptions
        logging.error(f"Integrity error: {e}")
    
    except sqlite3.Error as e:
        # Log general database errors
        logging.error(f"Database error: {e}")
    
    except Exception as e:
        # Handle unexpected errors
        logging.error(f"Unexpected error: {e}")
       
def test_add_airline():
    try:
        # Connect to the database using a context manager
        with sqlite3.connect(config.DATABASE_NAME) as conn:
            conn.row_factory = sqlite3.Row #Allow accessing rows as dictionary
            cursor = conn.cursor()

            #Generate a random name to be sure there are no conflicts
            name = str(uuid.uuid4())            
            
            cursor.execute(f"SELECT COUNT(*) from Airline where Name = ?",(name,))
            row = cursor.fetchone()
            assert row[0] == 0 # Ensure there are no airlines with this name
            
            #Add the airline
            airlines.add_airline(name,'bla bla','tyr123')
            cursor.execute(f"Select AirlineId,Name,IATACode,Terminal,IsActive from Airline where Name = ?",(name,))
            row = cursor.fetchone()
            assert row is not None 
            assert row["Name"] == name
            assert row["IATACode"] == "bla bla"
            assert row["Terminal"] == "tyr123"
            assert row["IsActive"] == util.ActiveStatus.ACTIVE.value

    except sqlite3.IntegrityError as e:
        # Handle specific SQLite exceptions
        logging.error(f"Integrity error: {e}")
    
    except sqlite3.Error as e:
        # Log general database errors
        logging.error(f"Database error: {e}")
    
    except Exception as e:
        # Handle unexpected errors
        logging.error(f"Unexpected error: {e}")

def test_amend_airline():
    try:
        # Connect to the database using a context manager
        with sqlite3.connect(config.DATABASE_NAME) as conn:
            conn.row_factory = sqlite3.Row #Allow accessing rows as dictionary
            cursor = conn.cursor()

            #Generate a random name to be sure there are no conflicts
            name = str(uuid.uuid4())            
            
            cursor.execute(f"SELECT COUNT(*) from Airline where Name = ?",(name,))
            row = cursor.fetchone()
            assert row[0] == 0 # Ensure there are no airlines with this name
            
            #Add the airline
            airlines.add_airline(name,'Bla Bla','tyr123',51)
            cursor.execute(f"Select AirlineId,Name,IATACode,Terminal,IsActive from Airline where Name = ?",(name,))
            row = cursor.fetchone()
            airlineId = row["AirlineId"]
            assert row is not None 
            assert row["Name"] == name
            assert row["IATACode"] == "Bla Bla"
            assert row["Terminal"] == "tyr123"
            assert row["IsActive"] == util.ActiveStatus.ACTIVE.value

            #Amend the airline
            name = str(uuid.uuid4())
            iataCode = str(uuid.uuid4())
            terminal= str(uuid.uuid4())
            isActive = util.ActiveStatus.INACTIVE.value
            airlines.amend_airline(airlineId,name,iataCode,terminal,isActive)

            #get the airline again and check that the values have been updated
            cursor.execute(f"Select AirlineId,Name,IATACode,Terminal,IsActive from Airline where AirlineId = ?",(airlineId,))
            row = cursor.fetchone()
            assert row is not None 
            assert row["Name"] == name
            assert row["IATACode"] == iataCode
            assert row["Terminal"] == terminal
            assert row["IsActive"] == isActive

    except sqlite3.IntegrityError as e:
        # Handle specific SQLite exceptions
        logging.error(f"Integrity error: {e}")
    
    except sqlite3.Error as e:
        # Log general database errors
        logging.error(f"Database error: {e}")
    
    except Exception as e:
        # Handle unexpected errors
        logging.error(f"Unexpected error: {e}")        
    