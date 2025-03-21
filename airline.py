import logging
import sqlite3
import config

def add_airline(name, IATACode, terminal):
    logging.info("add_airline started.")  # Corrected log message

    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(config.DATABASE_NAME)
        cursor = conn.cursor()
        
        # Execute SQL command with proper parameter substitution
        cursor.execute("""INSERT INTO Airline (Name, IATACode, Terminal) 
                          VALUES (?, ?, ?);""", (name, IATACode, terminal))
        
        # Commit the transaction
        conn.commit()
        logging.info("Airline added successfully.")
    
    except sqlite3.Error as e:
        # Log an error if something goes wrong
        logging.error(f"Error while adding airline: {e}")
    
    finally:
        # Close the connection in a `finally` block to ensure it always closes
        if conn:
            conn.close()
            logging.info("Database connection closed.")

    logging.info("add_airline completed.")      

def show_airlines():
    logging.info("show_airlines started.")
    conn = sqlite3.connect(config.DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Airline")
    rows = cursor.fetchall()
    for row in rows:
        print (row)
    conn.close()
    logging.info("show_airlines completed.")         
