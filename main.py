import datetime
import logging
import sqlite3
import menus

import setupdatabase as sd

# Configure logging
logging.basicConfig(
    level=logging.CRITICAL,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s"  # Customize log message format
)

# Sample log messages
# logging.debug("This is a DEBUG message.")
# logging.info("This is an INFO message.")
# logging.warning("This is a WARNING message.")
# logging.error("This is an ERROR message.")
# logging.critical("This is a CRITICAL message.")


def show_planes():
    logging.info("show_planes started.")
    conn = sqlite3.connect('awgsstore')
    now = datetime.datetime.now()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Plane")
    rows = cursor.fetchall()
    for row in rows:
        print (row)
    logging.info("show_planes completed.")
    


def show_destinations():
    logging.info("show_destinations started.")
    conn = sqlite3.connect('awgsstore')
    now = datetime.datetime.now()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Destination")
    rows = cursor.fetchall()
    for row in rows:
        print (row)
    logging.info("show_destinations completed.")    

def show_date_time():
    now = datetime.datetime.now()
    print(f"\nThe current date and time is: {now}")


def main():

    sd.cleanup_database()
    sd.setup_database()
    sd.setup_test_data()

    while True:
        print("\nChoose an option:")
        print("1. Pilot Management")
        print("2. Airline Management")
        print("3. Flight Management")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            menus.pilot_management_menu()
        elif choice == "2":
            menus.airline_management_menu()
        elif choice == "3":
            menus.flight_management_menu()
        elif choice == "4":
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()
