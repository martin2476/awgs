# Creates the temporary database and populates it with sample data 
import datetime
import random
import logging
import sqlite3
import config
import util

def cleanup_database():
    conn = sqlite3.connect(config.DATABASE_NAME)
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
    conn = sqlite3.connect(config.DATABASE_NAME)
    now = datetime.datetime.now()
    logging.info("Creating database.")
    
    cursor = conn.cursor()

    #SQLite does not have a dedicated date data type therefore using text so that it is human readable - YYYY-MM-DD HH:MM:SS
    #SQLite uses dynamic typing, so Text is being used which is more common in SQLite
    cursor.execute("""CREATE TABLE Pilot (
                 PilotID INTEGER PRIMARY KEY, 
                 Name TEXT, 
                 Surname TEXT, 
                 LicenseNumber TEXT,
                 Is_Active INTEGER NOT NULL CHECK (Is_Active IN (0,1))          -- 1 is active, 0 is not active
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
    
    #Flights under 8 hours normally have 2 pilots while flights above 8 hours can have 1 or 2 relief pilots
    #there I am using linkage table
    cursor.execute("""CREATE TABLE FlightPilots (
                 ID INTEGER PRIMARY KEY,
                 FlightID INTEGER,       -- Link to the flight
                 PilotID INTEGER,        -- Link to the pilot
                 UNIQUE (FlightID, PilotID) -- Composite Unique Key
                 );""")
    cursor.execute("""CREATE TABLE FlightDetails (
                 FlightID INTEGER PRIMARY KEY,       -- Unique ID for the flight
                 FlightName TEXT,                    -- 
                 PlaneID INTEGER,                    -- Link to the plane
                 OriginID INTEGER,                   -- Link to the origin destination
                 DestinationID INTEGER,              -- Link to the destination
                 ScheduledFlightDate TEXT,           -- Scheduled Date / Time of the flight (ISO-8601 format)
                 ActualFlightDate TEXT,              -- Actual Date / Time of the flight (ISO-8601 format)
                 DurationMinutes INTEGER,            -- Duration of the flight in minutes
                 Terminal TEXT,
                 Gate TEXT,
                 AirlineID INTEGER,                      -- The airline operating the flight
                 FlightStatus TEXT,                      -- the current flight status - FlightStatus enum
                 FOREIGN KEY (PlaneID) REFERENCES Planes(PlaneID),          -- Foreign key to Plane table
                 FOREIGN KEY (OriginID) REFERENCES Destinations(DestinationID), -- Foreign key to Destination table
                 FOREIGN KEY (DestinationID) REFERENCES Destinations(DestinationID) -- Foreign key to Destination table
                 FOREIGN KEY (AirlineID) REFERENCES Airlines(AirlineID) -- Foreign key to Airline table
            );""")
    
    conn.commit()
    conn.close()

def setup_test_data():
    conn = sqlite3.connect(config.DATABASE_NAME)
    now = datetime.datetime.now()
    logging.info("Database {conn.database} has been created.")
    
    cursor = conn.cursor()

    # Insert sample records into the Pilot table
    cursor.executemany("""
        INSERT INTO Pilot (PilotID, Name, Surname, LicenseNumber,Is_Active)
        VALUES (?, ?, ?, ?, ?);
    """, [
        (1, 'John', 'Smith', 'LN12345',util.ActiveStatus.ACTIVE.value),
        (2, 'Emily', 'Davis', 'LN23456',util.ActiveStatus.ACTIVE.value),
        (3, 'James', 'Taylor', 'LN34567',util.ActiveStatus.ACTIVE.value),
        (4, 'Olivia', 'Brown', 'LN45678',util.ActiveStatus.ACTIVE.value),
        (5, 'William', 'Johnson', 'LN56789',util.ActiveStatus.ACTIVE.value),
        (6, 'Sophia', 'Miller', 'LN67890',util.ActiveStatus.ACTIVE.value),
        (7, 'Liam', 'Wilson', 'LN78901',util.ActiveStatus.ACTIVE.value),
        (8, 'Mia', 'Moore', 'LN89012',util.ActiveStatus.ACTIVE.value),
        (9, 'Benjamin', 'Clark', 'LN90123',util.ActiveStatus.ACTIVE.value),
        (10, 'Charlotte', 'Hall', 'LN01234',util.ActiveStatus.ACTIVE.value),
        (11, 'Henry', 'Adams', 'LN13579',util.ActiveStatus.ACTIVE.value),
        (12, 'Ava', 'Johnson', 'LN24680',util.ActiveStatus.ACTIVE.value),
        (13, 'Noah', 'Evans', 'LN35791',util.ActiveStatus.ACTIVE.value),
        (14, 'Ella', 'Roberts', 'LN46802',util.ActiveStatus.ACTIVE.value),
        (15, 'Lucas', 'Garcia', 'LN57913',util.ActiveStatus.ACTIVE.value)
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
        (10, 'N-KLMN', 'Piper', 'M600', 'T0123', 6),
        (11, 'G-UVWX', 'Boeing', '747-400', 'T1357', 416),
        (12, 'N-YZAB', 'Airbus', 'A220-300', 'T2468', 141),
        (13, 'F-CDEF', 'Cessna', 'Skyhawk 172', 'T3579', 4),
        (14, 'D-GHIJ', 'Dassault', 'Falcon 2000', 'T4680', 19),
        (15, 'G-KLMN', 'Embraer', 'E175', 'T5791', 88)
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
        (10, 'São Paulo Guarulhos', 'Brazil', 'GRU', 5921),
        (11, 'Los Angeles International', 'United States', 'LAX', 8757),
        (12, 'Hong Kong International', 'Hong Kong', 'HKG', 5990),
        (13, 'Amsterdam Schiphol', 'Netherlands', 'AMS', 356),
        (14, 'Madrid Barajas', 'Spain', 'MAD', 785),
        (15, 'Mexico City International', 'Mexico', 'MEX', 5533),
        (16, 'Heathrow Airport', 'UK', 'LHR', 0)
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
        (10, 'Qantas', 'QF', '3' ),
        (11, 'Delta Air Lines', 'DL', '4'),
        (12, 'Turkish Airlines', 'TK', '3'),
        (13, 'Etihad Airways', 'EY', '4'),
        (14, 'Aer Lingus', 'EI', '2'),
        (15, 'Swiss International Air Lines', 'LX', '2')
    ])

    # Generate 15 sample records for FlightDetails
    sample_flight_details = []
    sample_pilot_flight_details = []

    for flight_id in range(1, 16):
        flight_name = f"Flight-{flight_id:03}"  # Example: Flight-001, Flight-002, etc.
        pilot_id = random.randint(1, 15)  # Random PilotID from 1 to 15
        copilot_id = random.randint(1, 15)  # Random PilotID from 1 to 15
        while (copilot_id == pilot_id):
            copilot_id = random.randint(1,15) # Copilot should be different from the Pilot
    
        plane_id = random.randint(1, 15)  # Random PlaneID from 1 to 15
        origin_id = 16                    # London Heathrow Airport is the hub and all flights originate from it
        destination_id = random.randint(1, 15)  # Random DestinationID from 1 to 15

        scheduled_date = (datetime.datetime.now() + datetime.timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d %H:%M:%S")
        actual_date = (datetime.datetime.now() + datetime.timedelta(days=random.randint(1, 30), hours=random.randint(0, 3))).strftime("%Y-%m-%d %H:%M:%S")
        """
        I should calculate the duration based on the destination distance
        """
        duration_minutes = random.randint(30, 720)  # Random duration from 30 minutes to 12 hours
        """
        The terminal should be coming from the airline
        """        
        terminal = random.choice(["1", "2", "3", "4", "5"])
        
        gate = random.choice(["A", "B", "C", "D"]) + str(random.randint(1, 10))  # Example: A3, B5, etc.
        airlineID = random.randint(1, 15)  # Random DestinationID from 1 to 15
        
        # Add record to the list
        sample_flight_details.append((
            flight_id,
            flight_name,
            plane_id,
            origin_id,
            destination_id,
            scheduled_date,
            actual_date,
            duration_minutes,
            terminal,
            gate,
            airlineID,
            util.FlightStatus.SCHEDULED.name
        ))

        sample_pilot_flight_details.append((
            flight_id,
            pilot_id
        ))        

    # Insert records into the FlightDetails table
    cursor.executemany("""
        INSERT INTO FlightDetails (
            FlightID, FlightName, PlaneID, OriginID, DestinationID, 
            ScheduledFlightDate, ActualFlightDate, DurationMinutes, Terminal, Gate, AirlineID, FlightStatus
        ) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, sample_flight_details)

    # Insert records into the FlightPilots table
    cursor.executemany("""
        INSERT INTO FlightPilots (
            FlightID, PilotID
        ) 
        VALUES (?, ?);
    """, sample_pilot_flight_details)

    #adding the copilot
    sample_pilot_flight_details.clear()
    sample_pilot_flight_details.append((
            flight_id,
            copilot_id
        ))       
    
    cursor.executemany("""
        INSERT INTO FlightPilots (
            FlightID, PilotID
        ) 
        VALUES (?, ?);
    """, sample_pilot_flight_details)

    conn.commit()
    conn.close()

    print("15 sample records added to the FlightDetails table.")