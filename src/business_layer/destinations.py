'''
    Contains all functions related to Destinations functionality
'''
import util
import databaseUtil

from tabulate import tabulate

@util.log_function_call
def show_destinations():
    records = databaseUtil.show_records("Destination")
    if records:
        print(tabulate(records, headers="keys", tablefmt="grid"))
    else:
        print("No records found.")    

@util.log_function_call
def add_destinations(name, country, airportCode,distanceFromLondon):
    databaseUtil.add_record(
    table_name="Destination",
    column_names=["Name", "Country", "AirportCode","DistanceFromLondon"],
    values=(name, country, airportCode,distanceFromLondon))