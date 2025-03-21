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
    logging.info("show_pilots completed.")