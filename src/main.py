import logging
import menus
import setupdatabase as sd
import databaseDAO as DatabaseDAO
import mytest


# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s"  # Customize log message format
    )


def main():

    sd.cleanup_database()
    sd.setup_database()
    sd.setup_test_data()


    #mytest.test_add_airplane()
    #mytest.test_amend_airplane()
    #mytest.test_delete_airplane()

    while True:
        print("\nChoose an option:")
        print("1. Pilot Management")
        print("2. Airline Management")
        print("3. Airplane Management")
        print("4. Destination Management")
        print("5. Flight Management")
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
        elif choice.upper() == "X":
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()
