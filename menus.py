import logging
import databaseUtil

def pilot_management_menu():
    while True:
        print("\n=== Pilot Management Menu ===")
        print("1. Add Pilot")
        print("2. View Pilots")
        print("3. View Pilot Schedule")
        print("X. Back to Main Menu")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            name = input("Enter the pilot's first name: ")
            surname = input("Enter the pilot's surname: ")
            licenseNumber = input("Enter the pilot's license number: ")
            databaseUtil.add_pilot(name,surname,licenseNumber)
        elif choice == "2":
            databaseUtil.show_pilots()
        elif choice == "3":
            logging.info("View pilot schedule.")
        elif choice.upper() == "X":
            break
        else:
            print("Invalid choice. Please try again.")

def airline_management_menu():
    while True:
        print("\n=== Airline Management Menu ===")
        print("1. Add Airline")
        print("2. View Airlines")
        print("X. Back to Main Menu")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            name = input("Enter the airline's name: ")
            iataCode = input("Enter the airline's IATA code: ")
            terminal = input("Enter the airline's terminal: ")
            databaseUtil.add_airline(name,iataCode,terminal)
        elif choice == "2":
            databaseUtil.show_airlines()
        elif choice.upper() == "X":
            break
        else:
            print("Invalid choice. Please try again.")

def airplane_management_menu():
    while True:
        print("\n=== Airplane Management Menu ===")
        print("1. Add Airplane")
        print("2. View Airplanes")
        print("X. Back to Main Menu")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            aircraftRegistrationNumber = input("Enter the airplane registration number: ")
            manufacturer = input("Enter the airplane's manufacturer: ")
            model = input("Enter the airplane's model: ")
            tailNumber = input("Enter the airplane's tail number: ")            
            capacity = input("Enter the airplane's capacity: ")            
            databaseUtil.add_airplane(aircraftRegistrationNumber,manufacturer,model,tailNumber,capacity)
        elif choice == "2":
            logging.info("Viewing all airplanes.")
            databaseUtil.show_airplanes()
        elif choice.upper() == "X":
            break
        else:
            print("Invalid choice. Please try again.")            

def destination_management_menu():
    while True:
        print("\n=== Destination Management Menu ===")
        print("1. Add Destination")
        print("2. View Destinations")
        print("X. Back to Main Menu")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            name = input("Enter the destination's name: ")
            country = input("Enter the destination's country: ")
            airportCode = input("Enter the destination's airport code: ")
            distanceFromLondon = input("Enter the destination's distance from London: ")            
            databaseUtil.show_destinations(name, country, airportCode,distanceFromLondon)
        elif choice == "2":
            databaseUtil.show_destinations()
        elif choice.upper() == "X":
            break
        else:
            print("Invalid choice. Please try again.")                

def flight_management_menu():
    while True:
        print("\n=== Flight Management Menu ===")
        print("1. Add Flight")
        print("2. View Flights")
        print("3. Update Flight")
        print("X. Back to Main Menu")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            logging.info("Adding a new flight.")
            # Placeholder for adding pilot logic
        elif choice == "2":
            logging.info("Viewing flights.")
            # Placeholder for viewing pilots logic
        elif choice == "3":
            logging.info("Update a flight.")
            # Placeholder for updating a flight            
        elif choice.upper() == "X":
            break
        else:
            print("Invalid choice. Please try again.")            