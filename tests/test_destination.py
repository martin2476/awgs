import uuid
import sqlite3
import logging
import src.util as util
import src.config as config
import src.business_layer.destinations as destinations

@util.log_function_call
def test_delete_destination():
    try:
        # Connect to the database using a context manager
        with sqlite3.connect(config.DATABASE_NAME) as conn:
            conn.row_factory = sqlite3.Row #Allow accessing rows as dictionary
            cursor = conn.cursor()
            
            #Generate a random name to be sure there are no conflicts
            name = str(uuid.uuid4())

            cursor.execute(f"SELECT COUNT(*) from Destination where Name = ?",(name,))
            row = cursor.fetchone()
            assert row[0] == 0 # Ensure there are no destinations with this name

            #Add the destination
            cursor.execute("""
                    INSERT INTO Destination (Name, Country, AirportCode,DistanceFromLondon,IsActive)
                    VALUES (?, ?, ?, ?, ?);
                """, 
                (name, 'bla bla', 'tyr123',51,util.ActiveStatus.ACTIVE.value))
            conn.commit()


            #Verify that the destination was inserted
            cursor.execute(f"Select DestinationId,Name from Destination where Name = ?",(name,))
            row = cursor.fetchone()
            assert row is not None 
            assert row["Name"] == name
           
            destinationId = row["DestinationID"]
            destinations.delete_destination(destinationId) #this has its own commit
            cursor.execute(f"SELECT COUNT(*) from Destination where DestinationId = ?",(destinationId,))
            row = cursor.fetchone()
            assert row[0] == 0 #Ensure the destination does no longer exists

    except sqlite3.IntegrityError as e:
        # Handle specific SQLite exceptions
        logging.error(f"Integrity error: {e}")
    
    except sqlite3.Error as e:
        # Log general database errors
        logging.error(f"Database error: {e}")
    
    except Exception as e:
        # Handle unexpected errors
        logging.error(f"Unexpected error: {e}")
       
def test_add_destination():
    try:
        # Connect to the database using a context manager
        with sqlite3.connect(config.DATABASE_NAME) as conn:
            conn.row_factory = sqlite3.Row #Allow accessing rows as dictionary
            cursor = conn.cursor()

            #Generate a random name to be sure there are no conflicts
            name = str(uuid.uuid4())            
            
            cursor.execute(f"SELECT COUNT(*) from Destination where Name = ?",(name,))
            row = cursor.fetchone()
            assert row[0] == 0 # Ensure there are no destinations with this name
            
            #Add the destination
            destinations.add_destination(name,'bla bla','tyr123',51)
            cursor.execute(f"Select DestinationId,Name,Country,AirportCode,DistanceFromLondon,IsActive from Destination where Name = ?",(name,))
            row = cursor.fetchone()
            assert row is not None 
            assert row["Name"] == name
            assert row["Country"] == "bla bla"
            assert row["AirportCode"] == "tyr123"
            assert row["DistanceFromLondon"] == 51
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

def test_amend_destination():
    try:
        # Connect to the database using a context manager
        with sqlite3.connect(config.DATABASE_NAME) as conn:
            conn.row_factory = sqlite3.Row #Allow accessing rows as dictionary
            cursor = conn.cursor()

            #Generate a random name to be sure there are no conflicts
            name = str(uuid.uuid4())            
            
            cursor.execute(f"SELECT COUNT(*) from Destination where Name = ?",(name,))
            row = cursor.fetchone()
            assert row[0] == 0 # Ensure there are no destinations with this name
            
            #Add the destination
            destinations.add_destination(name,'Bla Bla','tyr123',51)
            cursor.execute(f"Select DestinationId,Name,Country,AirportCode,DistanceFromLondon,IsActive from Destination where Name = ?",(name,))
            row = cursor.fetchone()
            destinationId = row["DestinationId"]
            assert row is not None 
            assert row["Name"] == name
            assert row["Country"] == "Bla Bla"
            assert row["AirportCode"] == "tyr123"
            assert row["DistanceFromLondon"] == 51
            assert row["IsActive"] == util.ActiveStatus.ACTIVE.value

            #Amend the destination
            name = str(uuid.uuid4())
            country = str(uuid.uuid4())
            airportCode= str(uuid.uuid4())
            distanceFromLondon= 99
            isActive = util.ActiveStatus.INACTIVE.value
            destinations.amend_destination(destinationId,name,country,airportCode,distanceFromLondon,isActive)

            #get the destination again and check that the values have been updated
            cursor.execute(f"Select DestinationId,Name,Country,AirportCode,DistanceFromLondon,IsActive from Destination where DestinationId = ?",(destinationId,))
            row = cursor.fetchone()
            assert row is not None 
            assert row["Name"] == name
            assert row["Country"] == country
            assert row["AirportCode"] == airportCode
            assert row["DistanceFromLondon"] == distanceFromLondon
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
    