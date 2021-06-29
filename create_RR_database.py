import mysql.connector
from mysql.connector import Error
from helper_functions import bbl_match_processing
import glob
from credentials import credentials


def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


# connect to the table test in the the database
HOST, USER, PASSWORD, DB_NAME = credentials()
connector = create_connection(HOST, USER, PASSWORD, DB_NAME)

# drop the table if it is already there
try:
    drop_table = """DROP TABLE overs"""
    execute_query(connector, drop_table)
except Error as e:
    print(f"The error '{e}' occurred")

# SQL command to set up the table
create_users_table = """
CREATE TABLE overs (
  id INT AUTO_INCREMENT, 
  rr FLOAT, 
  over_number INT,
  balls INT,
  runs INT,
  wickets INT, 
  ground TEXT, 
  date DATE,
  season INT,
  innings INT,
  batting_team TEXT,
  bowling_team TEXT,
  PRIMARY KEY(id)
) ENGINE = InnoDB
"""

execute_query(connector, create_users_table)

# iterate through matches adding data to table
files = [f for f in glob.glob("bbl/*.yaml")]
for the_match in files:
    # single iteration version
    # the_match = glob.glob('bbl/524915.yaml')[0]

    output = bbl_match_processing(the_match)

    # first fixed part of SQL command
    top_string = """
    INSERT INTO
    `overs` (`rr`, `over_number`, `balls`, `runs`, `wickets`, `ground`, `date`, `season`, `innings`, `batting_team`, `bowling_team`)
    VALUES
        """

    # generate and execute command for each over of each innings of each match
    for o in output:
        # second part of SQL command
        add_row_to_table = f"({o[1]}, {o[0]}, {o[2]}, {o[3]}, {o[4]}, '{o[5]}', '{o[6]}', {o[7]}, {o[8]}, '{o[9]}', '{o[10]}')"
        # entries in the o list: [OVER, RR,  N_BALLS, RUNS,  WICKETS,  GROUND,   DATE,   SEASON, INNINGS, BATTING_TEAM, BOWLING_TEAM]"
        # order of columns in table: rr, over_number, balls, runs, wickets, ground, date, season, innings, batting_team, bowling_team

        # add the data to the table
        execute_query(connector, top_string + add_row_to_table)

print('Finished')
