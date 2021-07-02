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
print([float(r[0]*6) for r in results])

# run-rate per ball separated by season of the BBL
select_query = f"SELECT season, over_number, 6*SUM(runs)/SUM(balls) avg_run_rate FROM test.overs" \
            f"GROUP BY season, over_number ORDER BY season, over_number; "
result = execute_read_query(connector, select_query)
RR_df = pd.DataFrame(result, columns=['season', 'over', 'RR'])
RR_df['RR'] = RR_df['RR'].apply(float)

# plot variance of run-rate per over from mean, separated by season
ax = sns.lineplot(data=RR_df, x='over', y='RR', hue='season')
ax.set(xlabel="over", ylabel="run-rate")
ax.legend(title="Season")
plt.show()
mean_RR = RR_df.groupby('over')['RR'].mean()
RR_df = RR_df.set_index('over')
RR_df['mean_RR'] = mean_RR
RR_df = RR_df.reset_index()
RR_df['RR_diff'] = RR_df['RR']-RR_df['mean_RR']
print(RR_df)

sns.set_theme(style="darkgrid")
palette = sns.color_palette("muted", 10)
ax = sns.lineplot(data=RR_df, x='over', y='RR_diff', hue='season', style='season', palette=palette)
ax.set(xlabel="over", ylabel="run-rate")
ax.legend(title="Season")
plt.show()

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
plt.show()
