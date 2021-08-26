import glob
import ruamel.yaml as yaml
from credentials import credentials
from SQL_functions import create_connection
from SQL_functions import execute_query
from SQL_functions import execute_read_query
from mysql.connector import Error
import re
import datetime

# This file connects to the bbl database, clears the existing tables,
# then processes bbl matches one-by-one, updating match, ball, and wicket data

# connect to the table bbl in the the database
HOST, USER, PASSWORD, DB_NAME = credentials()
connector = create_connection(HOST, USER, PASSWORD, DB_NAME)

# First drop the tables if it they are already there
Tables = ['match_info', 'ball_info', 'wicket_info']
for table in Tables:
    try:
        drop_table = f"DROP TABLE {table}"
        execute_query(connector, drop_table)
    except Error as e:
        print(f"The error '{e}' occurred")

# Now set up the three tables

create_match_table = """
CREATE TABLE match_info (
match_id INT,
season INT,
ground TEXT,
teamA TEXT,
teamB TEXT,
date DATE,
PRIMARY KEY(match_id)
) ENGINE = InnoDB
"""

create_balls_table = """
CREATE TABLE ball_info (
  ball_id INT AUTO_INCREMENT,
  match_id INT,
  over_number INT,
  ball_number INT,
  ball_number_in_innings INT,
  runs INT,
  score INT,
  wicket BOOLEAN,
  extra BOOLEAN,
  wicket_num INT,
  innings INT,
  batting_team TEXT,
  bowling_team TEXT,
  PRIMARY KEY(ball_id)
) ENGINE = InnoDB
"""

create_wickets_table = """
CREATE TABLE wicket_info (
  wicket_id INT AUTO_INCREMENT, 
  match_id INT,
  ball_id INT,
  player TEXT,
  method TEXT,
  PRIMARY KEY(wicket_id)
) ENGINE = InnoDB
"""

execute_query(connector, create_match_table)
execute_query(connector, create_balls_table)
execute_query(connector, create_wickets_table)

# Now we can populate the tables. Iterate through the matches, extracting the relevant data
for match in glob.iglob("bbl/*.yaml"):
    # single iteration version
    # the_match = glob.glob('bbl/524915.yaml')[0]

    with open(match) as stream:
        try:
            the_match = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    # match id (from the yaml filename) regex-es the numbers from the filename
    MATCH_ID = int(re.search("[\\d]+", match).group())
    GROUND = the_match['info']['venue']  # ground the game was played at
    if GROUND == 'Western Australia Cricket Association Ground':
        GROUND = 'W.A.C.A. Ground'
    elif GROUND == 'Brisbane Cricket Ground, Woolloongabba':
        GROUND = 'Brisbane Cricket Ground'
    if isinstance(the_match['info']['dates'][0], datetime.date):
        date_dt = the_match['info']['dates'][0]
    elif isinstance(the_match['info']['dates'][0], str):
        date_dt = datetime.datetime.strptime(the_match['info']['dates'][0], '%Y-%m-%d').date()
    DATE = date_dt.isoformat()
    # get season number from date (bbl season 1 was 2011/12)
    SEASON = int((date_dt - datetime.date(2010, 8, 1)) / datetime.timedelta(days=365))
    TEAM_A = the_match['info']['teams'][0]
    TEAM_B = the_match['info']['teams'][1]

    insert_match_query = f"""INSERT INTO `match_info` (`match_id`, `season`, `ground`, `teamA`, `teamB`, `date`) 
    VALUES ({MATCH_ID}, {SEASON}, '{GROUND}', '{TEAM_A}', '{TEAM_B}', '{DATE}')
    """
    execute_query(connector, insert_match_query)

    for innings in the_match['innings']:
        the_innings = innings[list(innings)[0]]
        INNINGS = 1 if list(innings)[0] == '1st innings' else 2
        BATTING_TEAM = the_innings['team']
        BOWLING_TEAM = TEAM_A if BATTING_TEAM != TEAM_A else TEAM_B
        BALL_NUMBER_IN_INNINGS = 0
        NUM_WICKETS = 0
        SCORE = 0
        for ball in the_innings['deliveries']:
            key_name = list(ball.keys())[0]  # delivery in the form a.b, 1.2 is the second ball in the second over
            OVER, BALL = [int(s) for s in str(key_name).split('.')]  # the number of completed overs
            RUNS = ball[key_name]['runs']['total']
            SCORE = SCORE + RUNS

            WICKET = True if 'wicket' in ball[key_name] else False
            EXTRA = True if 'extras' in ball[key_name] else False

            NUM_WICKETS = NUM_WICKETS + 1 if 'wicket' in ball[key_name] else NUM_WICKETS
            BALL_NUMBER_IN_INNINGS = BALL_NUMBER_IN_INNINGS + 1

            insert_ball_query = f"""INSERT INTO `ball_info` 
            (`match_id`, `over_number`, `ball_number`, `ball_number_in_innings`, `runs`, `score`, 
            `wicket`,`extra`, `wicket_num`, `innings`, `batting_team`, `bowling_team`) 
            VALUES ({MATCH_ID}, {OVER}, {BALL}, {BALL_NUMBER_IN_INNINGS}, {RUNS}, {SCORE}, 
            {WICKET}, {EXTRA}, {NUM_WICKETS}, {INNINGS}, '{BATTING_TEAM}', '{BOWLING_TEAM}')
            """

            execute_query(connector, insert_ball_query)

            if WICKET:
                PLAYER = ball[key_name]['wicket']['player_out'].replace("'", "''")
                METHOD = ball[key_name]['wicket']['kind']

                BALL_ID = execute_read_query(connector, f"""
                SELECT ball_id FROM `ball_info` 
                WHERE match_id={MATCH_ID} AND innings={INNINGS} AND ball_number_in_innings={BALL_NUMBER_IN_INNINGS}
                """)

                insert_wicket_query = f"""INSERT INTO `wicket_info` (`match_id`, `ball_id`, `player`, `method`) 
                VALUES ({MATCH_ID}, {BALL_ID[0][0]}, '{PLAYER}', '{METHOD}')
                """

                execute_query(connector, insert_wicket_query)
