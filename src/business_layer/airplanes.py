'''
    Contains all functions related to Airplanes functionality
'''
import util
import databaseUtil

from tabulate import tabulate

@util.log_function_call
def show_airplanes():
    records = databaseUtil.show_records("Plane")
    if records:
        print(tabulate(records, headers="keys", tablefmt="grid"))
    else:
        print("No records found.")

@util.log_function_call
def add_airplane(aircraftRegistrationNumber,manufacturer,model,tailNumber,capacity):
    databaseUtil.add_record(
    table_name="Plane",
    column_names=["AircraftRegistrationNumber", "Manufacturer", "Model","TailNumber","Capacity"],
    values=(aircraftRegistrationNumber,manufacturer,model,tailNumber,capacity))