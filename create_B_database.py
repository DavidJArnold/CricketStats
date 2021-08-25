from helper_functions import bbl_ball_processing
import glob
import re
from credentials import credentials
from SQL_functions import create_connection
from SQL_functions import execute_query
from mysql.connector import Error

# connect to the table test in the the database
HOST, USER, PASSWORD, DB_NAME = credentials()
connector = create_connection(HOST, USER, PASSWORD, DB_NAME)

# drop the table if it is already there
try:
    drop_table = """DROP TABLE balls"""
    execute_query(connector, drop_table)
except Error as e:
    print(f"The error '{e}' occurred")

# SQL command to set up the table
create_balls_table = """
CREATE TABLE balls (
  id INT AUTO_INCREMENT, 
  over_number INT,
  ball_number INT,
  season INT,
  score INT,
  wicket BOOLEAN,
  wicket_num INT,
  PRIMARY KEY(id)
) ENGINE = InnoDB
"""

execute_query(connector, create_balls_table)
N = 0
# iterate through matches adding data to table
for the_match in glob.iglob("bbl/*.yaml"):
    # single iteration version
    # the_match = glob.glob('bbl/524915.yaml')[0]

    output = bbl_ball_processing(the_match)

    # first fixed part of SQL command
    top_string = """INSERT INTO `balls` (`over_number`, `ball_number`, `season`, `score`, `wicket`, `wicket_num`) VALUES """
    N = N + len(output)
    # generate and execute command for each over of each ball of each match
    for o in output:
        # second part of SQL command
        add_row_to_table = f"({o[0]}, {o[1]}, {o[2]}, {o[3]}, {o[4]}, {o[5]}) "
        # entries in o :       OVER,   BALL,  SEASON, SCORE,  WICKET, NUM_WICKETS
        # columns in table:   over_number, ball_number, season, score, wicket, num_wickets

        # add the data to the table
        execute_query(connector, top_string + add_row_to_table)

print(f'Finished {N} records')
