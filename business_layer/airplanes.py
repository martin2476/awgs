'''
    Contains all functions related to Airplanes functionality
'''
import util
import databaseUtil

@util.log_function_call
def show_airplanes():
    databaseUtil.show_records("Plane")

@util.log_function_call
def add_airplane(aircraftRegistrationNumber,manufacturer,model,tailNumber,capacity):
    databaseUtil.add_record(
    table_name="Plane",
    column_names=["AircraftRegistrationNumber", "Manufacturer", "Model","TailNumber","Capacity"],
    values=(aircraftRegistrationNumber,manufacturer,model,tailNumber,capacity))