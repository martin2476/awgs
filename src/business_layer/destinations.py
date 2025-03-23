'''
    Contains all functions related to Destinations functionality
'''
import util
import databaseUtil

@util.log_function_call
def show_destinations():
    databaseUtil.show_records("Destination")

@util.log_function_call
def add_destinations(name, country, airportCode,distanceFromLondon):
    databaseUtil.add_record(
    table_name="Destination",
    column_names=["Name", "Country", "AirportCode","DistanceFromLondon"],
    values=(name, country, airportCode,distanceFromLondon))