import logging
import sqlite3
import config

def show_pilots():
    logging.info("show_pilots started.")
    conn = sqlite3.connect(config.DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Pilot")
    rows = cursor.fetchall()
    for row in rows:
        print (row)
    
    conn.close()
    logging.info("show_pilots completed.")

def add_pilot(name, surname, licenceNumber):
    logging.info("add_pilot started.")  # Corrected log message

    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(config.DATABASE_NAME)
        cursor = conn.cursor()
        
        # Execute SQL command with proper parameter substitution
        cursor.execute("""INSERT INTO Pilot (Name, Surname, LicenseNumber) 
                          VALUES (?, ?, ?);""", (name, surname, licenceNumber))
        
        # Commit the transaction
        conn.commit()
        logging.info("Pilot added successfully.")
    
    except sqlite3.Error as e:
        # Log an error if something goes wrong
        logging.error(f"Error while adding pilot: {e}")
    
    finally:
        # Close the connection in a `finally` block to ensure it always closes
        if conn:
            conn.close()
            logging.info("Database connection closed.")

    logging.info("add_pilot completed.")


def show_airplanes():
    logging.info("show_planes started.")
    conn = sqlite3.connect(config.DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Plane")
    rows = cursor.fetchall()
    for row in rows:
        print (row)
    conn.close()
    logging.info("show_planes completed.")

      