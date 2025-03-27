'''
    Contains all functions related to Airlines functionality
'''
import util

from tabulate import tabulate
from databaseDAO import DatabaseDAO

@util.log_function_call
def show_airlines():
    records = DatabaseDAO.get_records("Airline")
    if records:
        print(tabulate(records, headers="keys", tablefmt="grid"))
    else:
        print("No records found.")        

@util.log_function_call
def add_airline(name, iataCode, terminal):
    DatabaseDAO.add_record(
    table_name="Airline",
    column_names=["Name", "IATACode", "Terminal"],
    values=(name, iataCode, terminal))