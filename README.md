### CricketStats
A repository of Python code used to study ball-by-ball cricket data sourced from [cricsheet.org](cricsheet.org). The description of the Cricsheet yaml format can be found [here](https://cricsheet.org/format/yaml/#introduction-to-the-yaml-format).

## create_RR_database.py and look_at_database.py
These files create and interrogate (respectively) a MySQL database for over-by-over statistics for mens Big Bash matches. Ball-by-ball statistics are combined to give over-by-over information, and the table include fields such as run-rate (by over), over number in the innings, number of balls bowled in the over (including no balls and wides), number of legal balls bowled (excluding no balls and wides), runs scored, wickets lost, and match information such as ground, date, BBL season, first or second innings, batting team, and  bowling team. The look_at_database file loads up the table an via a range of SQL queries looks at statistics measured against different grouping variables.

## test_match_example.py
This file shows an example of how to work with the ball-by-ball data. It uses the archive of men's Test matches and counts the occurrences of wickets, wides, and no-balls for each delivery in an over. It also displays the result of games, parsing the vairous options for results/ties/etc.

## helper_functions.py and SQL_functions.py
These files contain utility functions used in other places. SQL_functions provides simple functions to create/add/query tables in databases. `helper_functions.py` contains most of the code used to work with the match yaml files to prepare data to be put into a database, or used directly in analysis.

### Dependencies
Requires `ruamel.yaml` to parse yaml files from Cricsheet.

The SQL functions require a file credentials.py which includes a function credentials() that returns four variables; HOST, USERNAME, PASSWORD, DB_NAME, which give the information required to connect to the database.
