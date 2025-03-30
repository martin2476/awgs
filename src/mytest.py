import uuid
import sqlite3
import logging
import util
import config as config
import databaseDAO as du
import business_layer.pilots as pilots



@util.log_function_call
def test_delete_pilot():
    try:
        # Connect to the database using a context manager
        with sqlite3.connect(config.DATABASE_NAME) as conn:
            conn.row_factory = sqlite3.Row #Allow accessing rows as dictionary
            cursor = conn.cursor()
            
            #Generate a random name to be sure there are no conflicts
            name = str(uuid.uuid4())

            cursor.execute(f"SELECT COUNT(*) from Pilot where Name = ?",(name,))
            row = cursor.fetchone()
            assert row[0] == 0 # Ensure there are no pilots with this name

            #Add the pilot
            cursor.execute("""
                    INSERT INTO Pilot (Name, Surname, LicenseNumber,IsActive)
                    VALUES (?, ?, ?, ?);
                """, 
                (name, 'Fenech', 'tyr123',util.ActiveStatus.ACTIVE.value))
            conn.commit()


            #Verify that the pilot was inserted
            cursor.execute(f"Select PilotId,Name from Pilot where Name = ?",(name,))
            row = cursor.fetchone()
            assert row is not None 
            assert row["Name"] == name
           
            pilotId = row["PilotID"]
            pilots.delete_pilot(pilotId) #this has its own commit
            cursor.execute(f"SELECT COUNT(*) from Pilot where PilotID = ?",(pilotId,))
            row = cursor.fetchone()
            assert row[0] == 0 #Ensure the pilot does no longer exists

    except sqlite3.IntegrityError as e:
        # Handle specific SQLite exceptions
        logging.error(f"Integrity error: {e}")
    
    except sqlite3.Error as e:
        # Log general database errors
        logging.error(f"Database error: {e}")
    
    except Exception as e:
        # Handle unexpected errors
        logging.error(f"Unexpected error: {e}")
       
def test_add_pilot():
    try:
        # Connect to the database using a context manager
        with sqlite3.connect(config.DATABASE_NAME) as conn:
            conn.row_factory = sqlite3.Row #Allow accessing rows as dictionary
            cursor = conn.cursor()

            #Generate a random name to be sure there are no conflicts
            name = str(uuid.uuid4())            
            
            cursor.execute(f"SELECT COUNT(*) from Pilot where Name = ?",(name,))
            row = cursor.fetchone()
            assert row[0] == 0 # Ensure there are no pilots with this name
            
            #Add the pilot
            pilots.add_pilot(name,'Fenech','tyr123')
            cursor.execute(f"Select PilotId,Name,Surname,LicenseNumber,IsActive from Pilot where Name = ?",(name,))
            row = cursor.fetchone()
            assert row is not None 
            assert row["Name"] == name
            assert row["Surname"] == "Fenech"
            assert row["LicenseNumber"] == "tyr123"
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

def test_amend_pilot():
    try:
        # Connect to the database using a context manager
        with sqlite3.connect(config.DATABASE_NAME) as conn:
            conn.row_factory = sqlite3.Row #Allow accessing rows as dictionary
            cursor = conn.cursor()

            #Generate a random name to be sure there are no conflicts
            name = str(uuid.uuid4())            
            
            cursor.execute(f"SELECT COUNT(*) from Pilot where Name = ?",(name,))
            row = cursor.fetchone()
            assert row[0] == 0 # Ensure there are no pilots with this name
            
            #Add the pilot
            pilots.add_pilot(name,'Fenech','tyr123')
            cursor.execute(f"Select PilotId,Name,Surname,LicenseNumber,IsActive from Pilot where Name = ?",(name,))
            row = cursor.fetchone()
            pilotId = row["PilotId"]
            assert row is not None 
            assert row["Name"] == name
            assert row["Surname"] == "Fenech"
            assert row["LicenseNumber"] == "tyr123"
            assert row["IsActive"] == util.ActiveStatus.ACTIVE.value

            #Amend the pilot
            name = str(uuid.uuid4())
            surname = str(uuid.uuid4())
            licenseNumber= str(uuid.uuid4())
            isActive = util.ActiveStatus.INACTIVE.value
            pilots.amend_pilot(pilotId,name,surname,licenseNumber,isActive)

            #get the pilot again and check that the values have been updated
            cursor.execute(f"Select PilotId,Name,Surname,LicenseNumber,IsActive from Pilot where PilotId = ?",(pilotId,))
            row = cursor.fetchone()
            assert row is not None 
            assert row["Name"] == name
            assert row["Surname"] == surname
            assert row["LicenseNumber"] == licenseNumber
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
    