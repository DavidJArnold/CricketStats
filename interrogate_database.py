import pandas as pd
from SQL_functions import execute_read_query
from SQL_functions import create_connection
from credentials import credentials

# get credentials and connect to a MySQL database
HOST, USER, PASSWORD, DB_NAME = credentials()
connector = create_connection(HOST, USER, PASSWORD, DB_NAME)

# For example, to get average run-rate per ball in each over across all games
select_query = "SELECT 6*AVG(runs) FROM ball_info GROUP BY over_number;"
results = execute_read_query(connector, select_query)
print([float(r[0]) for r in results])

# Run-rate per over separated by ground
select_query = """SELECT ground, over_number, 6*AVG(runs) avg_run_rate
                  FROM ball_info b JOIN match_info m ON b.match_id = m.match_id 
                  GROUP BY ground, over_number;"""
result = execute_read_query(connector, select_query)
print(result)
# And to convert to a dataframe
R_df = pd.DataFrame(result, columns=['ground', 'over', 'RR'])
R_df['RR'] = R_df['RR'].apply(float)
print(R_df.head())

# Look at the deviation from season to season of the run-rate in each over
full_query = """
WITH
    m1 AS (
        SELECT season, over_number, 6*SUM(runs)/COUNT(*) RR
        FROM ball_info b JOIN match_info m ON b.match_id=m.match_id
        GROUP BY season, over_number
        ),
    m2 AS (
        SELECT over_number, AVG(RR) mean
        FROM m1
        GROUP BY over_number)
SELECT m1.over_number, season, RR, mean, RR-mean deviation
FROM m1 JOIN m2 WHERE m1.over_number=m2.over_number
ORDER BY season, m1.over_number;
"""
result = execute_read_query(connector, full_query)
RR_df = pd.DataFrame(result, columns=['over', 'season', 'RR', 'mean_RR', 'RR_diff'])
RR_df.to_csv("run_rate_season.csv")
print(RR_df.head())

# Per-over wicket proportion
wickets_query = """
WITH 
    totals AS (SELECT m.season, COUNT(*) total
                FROM wicket_info w JOIN ball_info b JOIN match_info m 
                WHERE w.ball_id=b.ball_id AND m.match_id=w.match_id
                GROUP BY season)
SELECT m.season, b.over_number+1 over_number, COUNT(*) num_wickets, total, COUNT(*)/total proportion
FROM wicket_info w JOIN ball_info b JOIN match_info m JOIN totals 
WHERE w.match_id=m.match_id AND w.ball_id=b.ball_id AND m.season=totals.season
GROUP BY season, over_number
ORDER BY season, over_number;
"""
w_DF = pd.DataFrame(execute_read_query(connector, wickets_query),
                    columns=['season', 'over', 'wickets', 'total_wickets', 'proportion'])
print(w_DF.head())
w_DF.to_csv('wicket_balls.csv')
