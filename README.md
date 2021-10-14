# CricketStats
A repository of Python code used to study ball-by-ball cricket data sourced from [www.cricsheet.org](cricsheet.org). The description of the Cricsheet yaml format can be found [here](https://cricsheet.org/format/yaml/#introduction-to-the-yaml-format).

### `populate_databases.py` and `interrogate_database.py`
These files create and interrogate (respectively) MySQL databases for over-by-over statistics for mens Big Bash matches. The database contains three tables, one for match information (such as venue, date, and teams), one for information about each ball (including runs, extras, whether a wicket fell), and one for wicket information (including the player dismissed and the method of dismissal).

`interrogate_database.py` show some examples using SQL queries to retrieve data from the database. The results can be converted into DataFrames, and some of them are exported to csv files which can be imported into Tableau for further visualisations (or plotted using Python packages such as Seaborn).

### `bbl_queries.sql`
This SQL script file contains several example MySQL queries to show how the database can be used to obtain useful information.

###  `SQL_functions.py`
`SQL_functions.py` provides simple functions to create/add/query tables in databases. Some of these functions were modelled after examples from RealPython.com.

## Dependencies
Requires the package `ruamel.yaml` to parse yaml files from Cricsheet.

The SQL functions require a file `credentials.py` which includes a function `credentials()` that returns four variables; `HOST`, `USERNAME`, `PASSWORD`, `DB_NAME`, which give the information required to connect to the database. This is not a particularly secure method, and care should be taken if the database is remotely accessible.
