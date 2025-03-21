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
                 Manufacturer TEXT,
                 Model TEXT,  
                 TailNumber TEXT UNIQUE, 
                 Capacity TEXT
                 );""")
    cursor.execute("""CREATE TABLE Airline (
                 AirlineID INTEGER PRIMARY KEY,
                 Name TEXT,
                 IATACode TEXT,
                 Terminal TEXT
                 );""")
    cursor.execute("""CREATE TABLE Destination (
                 DestinationID INTEGER PRIMARY KEY,
                 Name TEXT,
                 Country TEXT,
                 AirportCode TEXT UNIQUE,
                 DistanceFromLondon INTEGER         --
                 );""")
    cursor.execute("""CREATE TABLE FlightDetails (
                 FlightID INTEGER PRIMARY KEY,       -- Unique ID for the flight
                 FlightName TEXT,                    -- 
                 PilotID INTEGER,                    -- Link to the pilot
                 PlaneID INTEGER,                    -- Link to the plane
                 OriginID INTEGER,                   -- Link to the origin destination
                 DestinationID INTEGER,              -- Link to the destination
                 ScheduledFlightDate TEXT,                    -- Scheduled Date / Time of the flight (ISO-8601 format)
                 ActualFlightDate TEXT,                    -- Actual Date / Time of the flight (ISO-8601 format)
                 DurationMinutes INTEGER,            -- Duration of the flight in minutes
                 Terminal TEXT,
                 Gate TEXT,
                 Airline TEXT,                      -- The airline operating the flight
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

    # Insert sample records into the Pilot table
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

    # Insert sample records into the Plane table
    cursor.executemany("""
        INSERT INTO Plane (PlaneID, AircraftRegistrationNumber, Manufacturer, Model, TailNumber, Capacity)
        VALUES (?, ?, ?, ?, ?, ?);
    """, [
        (1, 'G-ABCD', 'Boeing', '737-800', 'T1234', 189),
        (2, 'N-EFGH', 'Airbus', 'A320', 'T2345', 180),
        (3, 'F-IJKL', 'Cessna', 'Citation X', 'T3456', 12),
        (4, 'D-MNOP', 'Gulfstream', 'G550', 'T4567', 16),
        (5, 'G-QRST', 'Bombardier', 'Global 7500', 'T5678', 19),
        (6, 'N-UVWX', 'Boeing', '787-9', 'T6789', 296),
        (7, 'F-YZAB', 'Airbus', 'A350-900', 'T7890', 315),
        (8, 'D-CDEF', 'Dassault', 'Falcon 900', 'T8901', 14),
        (9, 'G-GHIJ', 'Embraer', 'Phenom 300', 'T9012', 10),
        (10, 'N-KLMN', 'Piper', 'M600', 'T0123', 6)
    ])

    # Insert sample records into the Destination table
    cursor.executemany("""
        INSERT INTO Destination (DestinationID, Name, Country, AirportCode,DistanceFromLondon)
        VALUES (?, ?, ?, ?,?);
    """, [
        (1, 'Paris Charles de Gaulle', 'France', 'CDG', 344),
        (2, 'New York John F. Kennedy', 'United States', 'JFK', 5570),
        (3, 'Tokyo Narita', 'Japan', 'NRT', 5973),
        (4, 'Dubai International', 'United Arab Emirates', 'DXB', 3405),
        (5, 'Sydney Kingsford Smith', 'Australia', 'SYD', 10563),
        (6, 'Singapore Changi', 'Singapore', 'SIN', 6762),
        (7, 'Cape Town International', 'South Africa', 'CPT', 6015),
        (8, 'Toronto Pearson', 'Canada', 'YYZ', 3557),
        (9, 'Frankfurt Airport', 'Germany', 'FRA', 406),
        (10, 'São Paulo Guarulhos', 'Brazil', 'GRU', 5921)
    ])    

    # Insert sample records into the Airline table
    cursor.executemany("""
        INSERT INTO Airline (AirlineID, Name, IATACode, Terminal)
        VALUES (?, ?, ?, ?);
""", [
    (1, 'British Airways', 'BA', '3, 5'),
    (2, 'Virgin Atlantic', 'VS', '3' ),
    (3, 'American Airlines', 'AA', '3' ),
    (4, 'Lufthansa', 'LH', '2' ),
    (5, 'Emirates', 'EK', '3' ),
    (6, 'Qatar Airways', 'QR', '4' ),
    (7, 'Singapore Airlines', 'SQ', '2' ),
    (8, 'Air Canada', 'AC', '2' ),
    (9, 'KLM Royal Dutch', 'KL', '4' ),
    (10, 'Qantas', 'QF', '3' )
])

    conn.commit()
    conn.close()
