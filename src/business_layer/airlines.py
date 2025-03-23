'''
    Contains all functions related to Airlines functionality
'''
import util
import databaseUtil

@util.log_function_call
def show_airlines():
    databaseUtil.show_records("Airline")

@util.log_function_call
def add_airline(name, iataCode, terminal):
    databaseUtil.add_record(
    table_name="Airline",
    column_names=["Name", "IATACode", "Terminal"],
    values=(name, iataCode, terminal))