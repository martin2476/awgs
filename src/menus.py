import logging
import databaseDAO as databaseDAO
import util
import business_layer.pilots as pilots
import business_layer.airlines as airlines
import business_layer.airplanes as airplanes
import business_layer.destinations as destinations
import business_layer.flights as flights

@util.log_function_call
def pilot_management_menu():
    while True:
        print("\n=== Pilot Management Menu ===")
        print("1. Add Pilot")
        print("2. Amend Pilot")
        print("3. Delete Pilot")
        print("4. View Pilots")
        print("5. View Pilot Schedule")
        print("6. View All Pilots Schedules")
        print("X. Back to Main Menu")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            name = input("Enter the pilot's first name: ")
            surname = input("Enter the pilot's surname: ")
            licenseNumber = input("Enter the pilot's license number: ")
            pilots.add_pilot(name,surname,licenseNumber)
        elif choice == "2":
            pilotId = input("Enter the pilot's id: ")
            pilots.amend_pilot(pilotId)
        elif choice == "3":
            pilotId = input("Enter the pilot's id: ")
            pilots.delete_pilot(pilotId)
        elif choice == "4":
            pilots.show_pilots()
        elif choice == "5":
            pilotId = input("Enter the pilot's id: ")
            pilots.show_pilot_schedule(pilotId)
        elif choice == "6":
            pilots.show_all_pilots_schedule()
        elif choice.upper() == "X":
            break
        else:
            print("Invalid choice. Please try again.")

@util.log_function_call
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
            airlines.add_airline(name,iataCode,terminal)
        elif choice == "2":
            airlineId = input("Enter the Airline's id: ")
            airlines.delete_airline(airlineId)
        elif choice == "3":
            airlineId = input("Enter the Airlines's id: ")
            airlines.amend_airline(airlineId)
        elif choice == "4":
            airlines.show_airlines()                  
        elif choice.upper() == "X":
            break
        else:
            print("Invalid choice. Please try again.")

@util.log_function_call
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
            airplanes.add_airplane(aircraftRegistrationNumber,manufacturer,model,tailNumber,capacity)
        elif choice == "2":
            airplaneId = input("Enter the Airplane's id: ")
            airplanes.amend_airplane(airplaneId)    
        elif choice == "3":
            airplaneId = input("Enter the Airplane's id: ")
            airplanes.delete_airplane(airplaneId)
        elif choice == "4":
            airplanes.show_airplanes()
        elif choice.upper() == "X":
            break
        else:
            print("Invalid choice. Please try again.")            

@util.log_function_call
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
            destinations.add_destinations(name, country, airportCode,distanceFromLondon)
        elif choice == "2":
            destinationId = input("Enter the Destination's id: ")
            destinations.amend_destination(destinationId)      
        elif choice == "3":
            destinationId = input("Enter the Destination's id: ")
            destinations.delete_destination(destinationId)
        elif choice == "4":
            destinations.show_destinations()
        elif choice.upper() == "X":
            break
        else:
            print("Invalid choice. Please try again.")                

@util.log_function_call
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
            update_flight_menu()
        elif choice == "3":
            logging.info("Delete a flight.")
            # Placeholder for updating a flight            
        elif choice == "4":
            flightName = input("Enter the Flight's name: ")
            flightDestination = input("Enter the Flight's destination: ")
            flightTerminal =  input("Enter the Flight's terminal: ")
            flightDate =  input("Enter the Flight's date: ")
            flightAirline =  input("Enter the Flight's Airline: ")
            flights.show_flights(flightName,flightDestination,flightTerminal,flightDate,flightAirline)
        elif choice.upper() == "X":
            break
        else:
            print("Invalid choice. Please try again.")            

@util.log_function_call
def update_flight_menu():
    while True:
        print("\n=== Update Flight Menu ===")
        print("1. Change Flight Status")
        print("2. Assign Pilot to Flight")
        print("3. Update Departure time")   
        print("4. Update Landing time")
        print("5. Assign gate")
        print("X. Back")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            flightId = input("Enter the Flight's id: ")
            for status in util.FlightStatus:
                print(f"{status.name} = {status.value}")
            statusId = input("Enter the Flight's status: ")
            flights.update_flight_status(flightId, util.FlightStatus(int(statusId)).name)
        elif choice == "2":
            #print out the pilots
            flightId = input("Enter the Flight's id: ")
            pilotId  = input("Enter the Pilot's id: ")
            flights.update_flight_pilot(flightId,pilotId)
        elif choice == "3":
#scheduled_date = (datetime.datetime.now() + datetime.timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d %H:%M:%S")
            flightId = input("Enter the Flight's id: ")
            statusId = input("Enter the Flight's status: ")
            flights.change_flight_status(flightId, util.FlightStatus(int(statusId)).name)
        elif choice == "4":
            pass
        elif choice == "5":
#scheduled_date = (datetime.datetime.now() + datetime.timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d %H:%M:%S")
            flightId = input("Enter the Flight's id: ")
            gateNumber = input("Enter the gate number: ")
            flights.update_flight_gate(flightId, gateNumber)
        elif choice.upper() == "X":
            break
        else:
            print("Invalid choice. Please try again.")

@util.log_function_call
def reporting_menu():
    while True:
        print("\n=== Reporting Menu ===")
        print("1. Number of flights per destination")
        print("X. Back")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            pass
        elif choice.upper() == "X":
            break
        else:
            print("Invalid choice. Please try again.")            