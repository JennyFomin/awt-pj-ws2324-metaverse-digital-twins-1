# -----------------
# NOT USED 
#
# This Python script executes an SQL script to create tables in an SQLite database. 
# It uses the sqlite3 library to manage the SQLite database connection and operations. 
# 
# -----------------

import sqlite3

def execute_sql_script(script_path):
    with open(script_path, 'r') as script_file:
        sql_script = script_file.read()
    
    # connect to database or create if not exist already 
    db_connection = sqlite3.connect("smart_home_data.db")

    cursor = db_connection.cursor()

    # create tables, if not exist already
    cursor.executescript(sql_script)

    # confirm changes in the database
    db_connection.commit()

    db_connection.close()

execute_sql_script('create_sqLite_tables.sql')
