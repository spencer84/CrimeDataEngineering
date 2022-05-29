import pandas as pd
import sqlite3

# Create a database
# If I had access to snowflake, I'd import the python module and connect to the db using the auth code

#
conn = sqlite3.connect("crime.db")

# Connect to DB

cur = conn.cursor()

# Create a table for the CSV Data

create_data_table = """CREATE TABLE IF NOT EXISTS crime 
(police_area text, month date, lng real, lat real, street text, crime_type text);"""

cur.execute(create_data_table)

# Create a secondary table to log when the primary table is updated

create_log_table = """CREATE TABLE IF NOT EXISTS crime_logs (police_area text, month date, update_date date, errors bool);"""

cur.execute(create_log_table)

crime_csv = pd.read_csv('crime.csv')

# If column name conventions differ from csv to db, provide mapping to correct formatting issues
col_mapping = {
    'Falls within':'police_area',
    'Month':'month',
    'Longitude':'lng',
    'Latitude':'lat',
    'Location':'street',
    'Crime type':'crime_type'
}

def find_file_paths():
    # Walk the directory and find all files with .csv in name

def csv_to_db(csv_paths, table_name,connection, col_mapping):
    """
    Write the contents of a given CSV file to a database
    :param csv_paths: Target paths to folder with CSV files to be uploaded
    :param connection: Database connection
    :param col_mapping: Dictionary for column name changes
    :return:
    """
    cur = connection.cursor()
    query = 'select * from ' + table_name + " limit 1"
    cur.execute(query)
    col_names = []
    for i in cur.description:
        col_names.append(i[0])  # Name of columns is first position for each description object, append to list
    for file in csv_paths:  # Iterate through the csv files in the list
        df = pd.read_csv(file)  # Read as Pandas DataFrame
        # Rename columns to match the database
        df.rename(columns=col_mapping, inplace=True)
        df = df[col_names]  # Return only the column names from the table and in the same order
        # Construct a query to insert data using the column names and values
        col_names = ', '.join(col_names)
        for i in df.values:  # Iterate through each row of values
            insert_query = "insert into " + table_name + " (" + col_names + ") VALUES " + str(tuple(i))
            cur.execute(insert_query)
    connection.commit()  # Commit all changes
    connection.close()  # Close the connection


# Read in downloaded crime statistics as a Pandas dataframe

# Write data to the database

