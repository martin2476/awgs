'''
    Contains all functions related to Airlines functionality
'''
import util
import databaseUtil

from tabulate import tabulate

@util.log_function_call
def show_airlines():
    records = databaseUtil.show_records("Airline")
    if records:
        print(tabulate(records, headers="keys", tablefmt="grid"))
    else:
        print("No records found.")        

@util.log_function_call
def add_airline(name, iataCode, terminal):
    databaseUtil.add_record(
    table_name="Airline",
    column_names=["Name", "IATACode", "Terminal"],
    values=(name, iataCode, terminal))