import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from SQL_functions import execute_read_query
from SQL_functions import create_connection
from credentials import credentials

# get credentials and connect to a MySQL database
HOST, USER, PASSWORD, DB_NAME = credentials()
connector = create_connection(HOST, USER, PASSWORD, DB_NAME)

# simple test to display 10 rows from the database
select_query = "SELECT * FROM test.overs LIMIT 10;"
results = execute_read_query(connector, select_query)
print(results)
for r in results:
    print(r)

# get average run-rate per ball in each over across all games
select_query = "SELECT SUM(runs)/SUM(balls) FROM test.overs GROUP BY over_number;"
results = execute_read_query(connector, select_query)
print([float(r[0] * 6) for r in results])

# run-rate per ball separated by season of the BBL
select_query = f"SELECT season, over_number, 6*SUM(runs)/SUM(balls) avg_run_rate FROM test.overs " \
               f"GROUP BY season, over_number ORDER BY season, over_number; "
result = execute_read_query(connector, select_query)
RR_df = pd.DataFrame(result, columns=['season', 'over', 'RR'])
RR_df['RR'] = RR_df['RR'].apply(float)

print(RR_df.head())

# plot variance of run-rate per over from mean, separated by season
ax = sns.lineplot(data=RR_df, x='over', y='RR', hue='season')
ax.set(xlabel="over", ylabel="run-rate")
ax.legend(title="Season")
# plt.show()
mean_RR = RR_df.groupby('over')['RR'].mean()
RR_df = RR_df.set_index('over')
RR_df['mean_RR'] = mean_RR
RR_df = RR_df.reset_index()
RR_df['RR_diff'] = RR_df['RR'] - RR_df['mean_RR']
print(RR_df)

RR_df.to_csv("run_rate_season.csv")

sns.set_theme(style="darkgrid")
palette = sns.color_palette("muted", 10)
ax = sns.lineplot(data=RR_df, x='over', y='RR_diff', hue='season', style='season', palette=palette)
ax.set(xlabel="over", ylabel="run-rate")
ax.legend(title="Season")
# plt.show()

# run-rate per over separated by ground
select_query = """SELECT ground, over_number, 6*SUM(runs)/SUM(balls) avg_run_rate 
FROM test.overs GROUP BY ground, over_number;"""
result = execute_read_query(connector, select_query)
print(result)
R_df = pd.DataFrame(result, columns=['ground', 'over', 'RR'])
R_df['RR'] = R_df['RR'].apply(float)
print(R_df)

ax = sns.lineplot(data=R_df, x='over', y='RR', hue='ground')
ax.set(xlabel="over", ylabel="run-rate")

ax.legend(title="Ground")
# plt.show()


# RR_df can also be created directly from an SQL query
full_query = """
WITH 
    m1 AS (
        SELECT season, over_number, 6*SUM(runs)/SUM(balls) RR 
        FROM overs 
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
print(pd.DataFrame(result, columns=['over', 'season', 'RR', 'mean_RR', 'RR_diff']).head())

# query wickets table to get per-ball wicket proportion
wickets_query = """
WITH 
	m1 AS (SELECT season, COUNT(*) total FROM wickets GROUP BY season)
SELECT wickets.season, over_number+1 over_num,  COUNT(*)/total proportion 
FROM wickets JOIN m1 WHERE m1.season=wickets.season 
GROUP BY wickets.season, wickets.over_number
ORDER BY wickets.season, wickets.over_number;
"""

w_DF = pd.DataFrame(execute_read_query(connector, wickets_query), columns=['season', 'over', 'proportion'])
print(w_DF.head())

w_DF.to_csv('wicket_balls.csv')
