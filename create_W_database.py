from helper_functions import bbl_wicket_processing
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
    drop_table = """DROP TABLE wickets"""
    execute_query(connector, drop_table)
except Error as e:
    print(f"The error '{e}' occurred")

# SQL command to set up the table
create_wickets_table = """
CREATE TABLE wickets (
  id INT AUTO_INCREMENT, 
  match_id INT,
  over_number INT,
  ball_number INT,
  player TEXT,
  method TEXT,
  ground TEXT, 
  date DATE,
  season INT,
  innings INT,
  batting_team TEXT,
  bowling_team TEXT,
  PRIMARY KEY(id)
) ENGINE = InnoDB
"""

execute_query(connector, create_wickets_table)

# iterate through matches adding data to table
for the_match in glob.iglob("bbl/*.yaml"):
    # single iteration version
    # the_match = glob.glob('bbl/524915.yaml')[0]

    output = bbl_wicket_processing(the_match)

    # match id (from the yaml filename) regex-es the numbers from the filename
    match_id = int(re.search("[\\d]+", the_match).group())

    # first fixed part of SQL command
    top_string = """INSERT INTO `wickets` (`match_id`, `over_number`, `ball_number`, `player`, `method`, 
     `ground`, `date`, `season`, `innings`, `batting_team`, `bowling_team`) VALUES """

    # generate and execute command for each over of each innings of each match
    for o in output:
        # second part of SQL command
        add_row_to_table = f"({match_id}, {o[0]}, {o[1]}, '{o[2]}', '{o[3]}', '{o[4]}', '{o[5]}', {o[6]}, {o[7]}, '{o[8]}', '{o[9]}') "
        # entries in o :                   [OVER, BALL,   PLAYER,  METHOD,     GROUND,   DATE,  SEASON, INNINGS, BATTING_TEAM, BOWLING_TEAM]
        # columns in table: match_id, over_number, ball_number, player, method, ground, date, season, innings, batting_team, bowling_team

        # add the data to the table
        execute_query(connector, top_string + add_row_to_table)

print('Finished')
