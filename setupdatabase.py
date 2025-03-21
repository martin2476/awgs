# Creates the temporary database and populates it with sample data 
import datetime
import logging
import sqlite3

def cleanup_database():
    conn = sqlite3.connect('awgsstore')
    now = datetime.datetime.now()
    logging.info("Deleting all tables.")
    
    cursor = conn.cursor()
    # Retrieve the names of all tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Drop each table
    for table_name in tables:
        table_name = table_name[0]  # Extract the name from the tuple
        cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
        print(f"Table '{table_name}' dropped.")

    # Commit changes and close the connection
    conn.commit()
    conn.close()

def setup_database():
    conn = sqlite3.connect('awgsstore')
    now = datetime.datetime.now()
    logging.info("Creating database.")
    
    cursor = conn.cursor()

    #SQLite does not have a dedicated date data type therefore using text so that it is human readable - YYYY-MM-DD HH:MM:SS
    #SQLite uses dynamic typing, so Text is being used which is more common in SQLite
    cursor.execute("""CREATE TABLE Pilot (
                 PilotID INTEGER PRIMARY KEY, 
                 Name TEXT, 
                 Surname TEXT, 
                 LicenseNumber TEXT
                 );""")
    cursor.execute("""CREATE TABLE Plane (
                 PlaneID INTEGER PRIMARY KEY,
                 AircraftRegistrationNumber TEXT, 
                 Model TEXT, Manufacturer , 
                 TailNumber TEXT UNIQUE, 
                 Capacity TEXT
                 );""")
    cursor.execute("""CREATE TABLE Destination (
                 DestinationID INTEGER PRIMARY KEY,
                 Name TEXT,
                 Country TEXT,
                 AirportCode TEXT UNIQUE
                 );""")
    cursor.execute("""CREATE TABLE FlightDetails (
                 FlightID INTEGER PRIMARY KEY,       -- Unique ID for the flight
                 PilotID INTEGER,                    -- Link to the pilot
                 PlaneID INTEGER,                    -- Link to the plane
                 OriginID INTEGER,                   -- Link to the origin destination
                 DestinationID INTEGER,              -- Link to the destination
                 FlightDate TEXT,                    -- Date of the flight (ISO-8601 format)
                 DurationMinutes INTEGER,            -- Duration of the flight in minutes
                 FOREIGN KEY (PilotID) REFERENCES Pilots(PilotID),          -- Foreign key to Pilots table
                 FOREIGN KEY (PlaneID) REFERENCES Planes(PlaneID),          -- Foreign key to Planes table
                 FOREIGN KEY (OriginID) REFERENCES Destinations(DestinationID), -- Foreign key to Destinations table
                 FOREIGN KEY (DestinationID) REFERENCES Destinations(DestinationID) -- Foreign key to Destinations table
            );""")
    
    conn.commit()
    conn.close()

def setup_test_data():
    conn = sqlite3.connect('awgsstore')
    now = datetime.datetime.now()
    logging.info("Database {conn.database} has been created.")
    
    cursor = conn.cursor()

    # Insert sample records
    cursor.executemany("""
        INSERT INTO Pilot (PilotID, Name, Surname, LicenseNumber)
        VALUES (?, ?, ?, ?);
    """, [
        (1, 'John', 'Smith', 'LN12345'),
        (2, 'Emily', 'Davis', 'LN23456'),
        (3, 'James', 'Taylor', 'LN34567'),
        (4, 'Olivia', 'Brown', 'LN45678'),
        (5, 'William', 'Johnson', 'LN56789'),
        (6, 'Sophia', 'Miller', 'LN67890'),
        (7, 'Liam', 'Wilson', 'LN78901'),
        (8, 'Mia', 'Moore', 'LN89012'),
        (9, 'Benjamin', 'Clark', 'LN90123'),
        (10, 'Charlotte', 'Hall', 'LN01234')
    ])

    conn.commit()
    conn.close()
