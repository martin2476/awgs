import logging
import sqlite3
import config

def add_destination(name, country, airportCode,distanceFromLondon):
    logging.info("add_destination started.")  # Corrected log message

    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(config.DATABASE_NAME)
        cursor = conn.cursor()
        
        # Execute SQL command with proper parameter substitution
        cursor.execute("""INSERT INTO Destination (Name, Country, AirportCode,DistanceFromLondon) 
                          VALUES (?, ?, ?,?);""", (name, country, airportCode,distanceFromLondon))
        
        # Commit the transaction
        conn.commit()
        logging.info("Destination added successfully.")
    
    except sqlite3.Error as e:
        # Log an error if something goes wrong
        logging.error(f"Error while adding destination: {e}")
    
    finally:
        # Close the connection in a `finally` block to ensure it always closes
        if conn:
            conn.close()
            logging.info("Database connection closed.")

    logging.info("add_destination completed.")      

def show_destinations():
    logging.info("show_destinations started.")
    conn = sqlite3.connect(config.DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Destination")
    rows = cursor.fetchall()
    for row in rows:
        print (row)
    conn.close()
    logging.info("show_destinations completed.")  