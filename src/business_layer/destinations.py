'''
    Contains all functions related to Destinations functionality
'''
import util
import databaseDAO as databaseDAO

from tabulate import tabulate

@util.log_function_call
def show_destinations():
    records = databaseDAO.get_records("Destination")
    if records:
        print(tabulate(records, headers="keys", tablefmt="grid"))
    else:
        print("No records found.")    

@util.log_function_call
def add_destinations(name, country, airportCode,distanceFromLondon):
    databaseDAO.add_record(
    table_name="Destination",
    column_names=["Name", "Country", "AirportCode","DistanceFromLondon"],
    values=(name, country, airportCode,distanceFromLondon))