import uuid
import sqlite3
import logging
import src.util as util
import src.config as config
import src.business_layer.airplanes as airplanes

@util.log_function_call
def test_delete_airplane():
    try:
        # Connect to the database using a context manager
        with sqlite3.connect(config.DATABASE_NAME) as conn:
            conn.row_factory = sqlite3.Row #Allow accessing rows as dictionary
            cursor = conn.cursor()
            
            #Generate a random Aircraft Registration Number to be sure there are no conflicts
            arn = str(uuid.uuid4())

            cursor.execute(f"SELECT COUNT(*) from Plane where AircraftRegistrationNumber = ?",(arn,))
            row = cursor.fetchone()
            assert row[0] == 0 # Ensure there are no airplanes with this Aircraft Registration Number

            #Add the airplane
            cursor.execute("""
                    INSERT INTO Plane (AircraftRegistrationNumber, Manufacturer, Model,TailNumber,Capacity,IsActive)
                    VALUES (?, ?, ?, ?, ?, ?);
                """, 
                (arn, 'bla bla', 'some model','tyr123',250,util.ActiveStatus.ACTIVE.value))
            conn.commit()


            #Verify that the airplane was inserted
            cursor.execute(f"Select PlaneId,AircraftRegistrationNumber from Plane where AircraftRegistrationNumber = ?",(arn,))
            row = cursor.fetchone()
            assert row is not None 
            assert row["AircraftRegistrationNumber"] == arn
           
            airplaneId = row["PlaneID"]
            airplanes.delete_airplane(airplaneId) #this has its own commit
            cursor.execute(f"SELECT COUNT(*) from Plane where PlaneId = ?",(airplaneId,))
            row = cursor.fetchone()
            assert row[0] == 0 #Ensure the airplane does no longer exists

    except sqlite3.IntegrityError as e:
        # Handle specific SQLite exceptions
        logging.error(f"Integrity error: {e}")
    
    except sqlite3.Error as e:
        # Log general database errors
        logging.error(f"Database error: {e}")
    
    except Exception as e:
        # Handle unexpected errors
        logging.error(f"Unexpected error: {e}")
       
def test_add_airplane():
    try:
        # Connect to the database using a context manager
        with sqlite3.connect(config.DATABASE_NAME) as conn:
            conn.row_factory = sqlite3.Row #Allow accessing rows as dictionary
            cursor = conn.cursor()

            #Generate a random Aircraft Registration Number to be sure there are no conflicts
            arn = str(uuid.uuid4())            
            
            cursor.execute(f"SELECT COUNT(*) from Plane where AircraftRegistrationNumber = ?",(arn,))
            row = cursor.fetchone()
            assert row[0] == 0 # Ensure there are no airplanes with this Aircraft Registration Number
            
            #Add the airplane
            airplanes.add_airplane(arn,'bla bla','tyr123','sdf324',215)
            cursor.execute(f"Select PlaneId,AircraftRegistrationNumber,Manufacturer,Model,TailNumber,Capacity,IsActive from Plane where AircraftRegistrationNumber = ?",(arn,))
            row = cursor.fetchone()
            assert row is not None 
            assert row["AircraftRegistrationNumber"] == arn
            assert row["Manufacturer"] == "bla bla"
            assert row["Model"] == "tyr123"
            assert row["TailNumber"] == "sdf324"
            assert row["Capacity"] == '215'
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

def test_amend_airplane():
    try:
        # Connect to the database using a context manager
        with sqlite3.connect(config.DATABASE_NAME) as conn:
            conn.row_factory = sqlite3.Row #Allow accessing rows as dictionary
            cursor = conn.cursor()

            #Generate a random aircraft registration number to be sure there are no conflicts
            arn = str(uuid.uuid4())            
            
            cursor.execute(f"SELECT COUNT(*) from Plane where AircraftRegistrationNumber = ?",(arn,))
            row = cursor.fetchone()
            assert row[0] == 0 # Ensure there are no airplanes with this Aircraft Registration Number
            
            #Add the airplane
            airplanes.add_airplane(arn,'Bla Bla','tyr123','kkllp',51)
            cursor.execute(f"Select PlaneID,AircraftRegistrationNumber,Manufacturer,Model,TailNumber,Capacity,IsActive from Plane where AircraftRegistrationNumber = ?",(arn,))
            row = cursor.fetchone()
            airplaneId = row["PlaneID"]
            assert row is not None 
            assert row["AircraftRegistrationNumber"] == arn
            assert row["Manufacturer"] == "Bla Bla"
            assert row["Model"] == "tyr123"
            assert row["Tailnumber"] == "kkllp"
            assert row["Capacity"] == '51'
            assert row["IsActive"] == util.ActiveStatus.ACTIVE.value

            #Amend the airplane
            arn = str(uuid.uuid4())
            manufacturer = str(uuid.uuid4())
            model= str(uuid.uuid4())
            tailNumber= str(uuid.uuid4())
            capacity= 598
            isActive = util.ActiveStatus.INACTIVE.value
            airplanes.amend_airplane(airplaneId,arn,manufacturer,model,tailNumber,capacity,isActive)

            #get the airplane again and check that the values have been updated
            cursor.execute(f"Select PlaneID,AircraftRegistrationNumber,Manufacturer,Model,TailNumber, Capacity,IsActive from Plane where PlaneId = ?",(airplaneId,))
            row = cursor.fetchone()
            assert row is not None 

            assert row["AircraftRegistrationNumber"] == arn
            assert row["Manufacturer"] == manufacturer
            assert row["Model"] == model
            assert row["Tailnumber"] == tailNumber
            assert row["Capacity"] == str(capacity)
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
    