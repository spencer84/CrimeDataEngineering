import pandas as pd
import sqlite3

# Create a database
# If I had access to snowflake, I'd import the python module and connect to the db using the auth code

#
conn = sqlite3.connect("crime.db")

# Connect to DB

cur = conn.cursor()

# Create a table for the CSV Data

create_data_table = """CREATE TABLE crime IF NOT EXISTS;"""

cur.execute(create_data_table)

# Create a secondary table to log when the primary table is updated

create_log_table = """CREATE TABLE crime_logs IF NOT EXISTS;"""

cur.execute(create_log_table)

crime_csv = pd.read_csv('crime.csv')

def csv_to_snowflake(csv_file):
    """
    
    :param csv_file:
    :return:
    """

# Read in downloaded crime statistics as a Pandas dataframe

# Write data to the database
