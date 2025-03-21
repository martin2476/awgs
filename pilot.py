import datetime
import logging
import sqlite3

def show_pilots():
    logging.info("show_pilots started.")
    conn = sqlite3.connect('awgsstore')
    now = datetime.datetime.now()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Pilot")
    rows = cursor.fetchall()
    for row in rows:
        print (row)
    conn.close()
    logging.info("show_pilots completed.")

def show_airlines():
    logging.info("show_airlines started.")
    conn = sqlite3.connect('awgsstore')
    now = datetime.datetime.now()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Airline")
    rows = cursor.fetchall()
    for row in rows:
        print (row)
    conn.close()
    logging.info("show_airlines completed.")        

def show_airplanes():
    logging.info("show_planes started.")
    conn = sqlite3.connect('awgsstore')
    now = datetime.datetime.now()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Plane")
    rows = cursor.fetchall()
    for row in rows:
        print (row)
    conn.close()
    logging.info("show_planes completed.")

def show_destinations():
    logging.info("show_destinations started.")
    conn = sqlite3.connect('awgsstore')
    now = datetime.datetime.now()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Destination")
    rows = cursor.fetchall()
    for row in rows:
        print (row)
    conn.close()
    logging.info("show_destinations completed.")        