import logging
import databaseUtil

def pilot_management_menu():
    while True:
        print("\n=== Pilot Management Menu ===")
        print("1. Add Pilot")
        print("2. Amend Pilot")
        print("3. Delete Pilot")
        print("4. View Pilots")
        print("5. View Pilot Schedule")
        print("X. Back to Main Menu")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            name = input("Enter the pilot's first name: ")
            surname = input("Enter the pilot's surname: ")
            licenseNumber = input("Enter the pilot's license number: ")
            databaseUtil.add_pilot(name,surname,licenseNumber)
        elif choice == "2":
            pilotId = input("Enter the pilot's id: ")
            databaseUtil.amend_pilot(pilotId)
        elif choice == "3":
            pilotId = input("Enter the pilot's id: ")
            databaseUtil.delete_pilot(pilotId)
        elif choice == "4":
            databaseUtil.show_pilots()
        elif choice == "5":
            pilotId = input("Enter the pilot's id: ")
            databaseUtil.show_pilot_schedule(pilotId)
        elif choice.upper() == "X":
            break
        else:
            print("Invalid choice. Please try again.")

def airline_management_menu():
    while True:
        print("\n=== Airline Management Menu ===")
        print("1. Add Airline")
        print("2. Amend Airline")        
        print("3. Delete Airline")
        print("4. View Airlines")        
        print("X. Back to Main Menu")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            name = input("Enter the airline's name: ")
            iataCode = input("Enter the airline's IATA code: ")
            terminal = input("Enter the airline's terminal: ")
            databaseUtil.add_airline(name,iataCode,terminal)
        elif choice == "2":
            airlineId = input("Enter the Airline's id: ")
            databaseUtil.delete_airline(airlineId)
        elif choice == "3":
            airlineId = input("Enter the Airlines's id: ")
            databaseUtil.amend_airline(airlineId)
        elif choice == "4":
            databaseUtil.show_airlines()                  
        elif choice.upper() == "X":
            break
        else:
            print("Invalid choice. Please try again.")

def airplane_management_menu():
    while True:
        print("\n=== Airplane Management Menu ===")
        print("1. Add Airplane")
        print("2. Amend Airplane")
        print("3. Delete Airplane")
        print("4. View Airplanes")
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
            airplaneId = input("Enter the Airplane's id: ")
            databaseUtil.amend_airplane(airplaneId)    
        elif choice == "3":
            airplaneId = input("Enter the Airplane's id: ")
            databaseUtil.delete_airplane(airplaneId)
        elif choice == "4":
            databaseUtil.show_airplanes()
        elif choice.upper() == "X":
            break
        else:
            print("Invalid choice. Please try again.")            

def destination_management_menu():
    while True:
        print("\n=== Destination Management Menu ===")
        print("1. Add Destination")
        print("2. Amend Destination")
        print("3. Delete Destination")
        print("4. View Destinations")
        print("X. Back to Main Menu")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            name = input("Enter the destination's name: ")
            country = input("Enter the destination's country: ")
            airportCode = input("Enter the destination's airport code: ")
            distanceFromLondon = input("Enter the destination's distance from London: ")            
            databaseUtil.add_destinations(name, country, airportCode,distanceFromLondon)
        elif choice == "2":
            destinationId = input("Enter the Destination's id: ")
            databaseUtil.amend_destination(destinationId)      
        elif choice == "3":
            destinationId = input("Enter the Destination's id: ")
            databaseUtil.delete_destination(destinationId)
        elif choice == "4":
            databaseUtil.show_destinations()
        elif choice.upper() == "X":
            break
        else:
            print("Invalid choice. Please try again.")                

def flight_management_menu():
    while True:
        print("\n=== Flight Management Menu ===")
        print("1. Add Flight")
        print("2. Amend Flight")
        print("3. Delete Flight")        
        print("4. View Flights")        
        print("X. Back to Main Menu")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            logging.info("Adding a new flight.")
            # Placeholder for adding pilot logic
        elif choice == "2":
            logging.info("Update a flight.")
            # Placeholder for updating a flight            
        elif choice == "3":
            logging.info("Delete a flight.")
            # Placeholder for updating a flight            
        elif choice == "4":
            logging.info("Viewing flights.")
            databaseUtil.show_flights()
        elif choice.upper() == "X":
            break
        else:
            print("Invalid choice. Please try again.")            