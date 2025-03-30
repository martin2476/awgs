import logging
import menus
import setupdatabase as sd
import mytest


# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s"  # Customize log message format
    )
    
# Sample log messages
# logging.debug("This is a DEBUG message.")
# logging.info("This is an INFO message.")
# logging.warning("This is a WARNING message.")
# logging.error("This is an ERROR message.")
# logging.critical("This is a CRITICAL message.")

    
def main():

    sd.cleanup_database()
    sd.setup_database()
    sd.setup_test_data()

    #mytest.test_delete_pilot()
    mytest.test_add_pilot()

    while True:
        print("\nChoose an option:")
        print("1. Pilot Management")
        print("2. Airline Management")
        print("3. Airplane Management")
        print("4. Destination Management")
        print("5. Flight Management")
        print("6. Reporting")
        print("X. Exit")

        choice = input("Enter your choice (1-5 || X): ")

        if choice == "1":
            menus.pilot_management_menu()
        elif choice == "2":
            menus.airline_management_menu()
        elif choice == "3":
            menus.airplane_management_menu()
        elif choice == "4":
            menus.destination_management_menu()
        elif choice == "5":
            menus.flight_management_menu()
        elif choice == "6":
            menus.reporting_menu()            
        elif choice.upper() == "X":
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()
