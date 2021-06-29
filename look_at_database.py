from mysql.connector import Error
import mysql.connector
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


connect = mysql.connector.connect(
            host="DESKTOP-O6496Q6",
            user="admin",
            passwd="computer123",
            database="test"
        )
#
select_query = "SELECT * FROM test.overs LIMIT 10;"
results = execute_read_query(connect, select_query)

print(results)
for r in results:
    print(r)


select_query = "SELECT SUM(runs)/SUM(balls) FROM test.overs GROUP BY over_number;"
results = execute_read_query(connect, select_query)
print([float(r[0]*6) for r in results])
# cursor = connect.cursor()
# cursor.execute(select_query)
# result = cursor.fetchall()
# print([float(r[0])*6 for r in result])

A = []
for s in range(1, 11):
    select_query = f"SELECT SUM(runs)/SUM(balls) FROM test.overs WHERE season = {s} GROUP BY over_number;"
    result = execute_read_query(connect, select_query)
    A.append([float(r[0])*6 for r in result])

R_df = pd.DataFrame(A, columns=['1', '2', '3', '4', '5', '6', ',7', '8', '9', '10', '11', '12', '13',
                                '14', '15', '16', '17', '18', '19', '20'], index=range(1, 11))
R_df.assign()
print(R_df)

ax = sns.lineplot(data=R_df.transpose())
ax.set(xlabel="over", ylabel="run-rate")
ax.legend(title="Season")
plt.show()

# A = []
# select_query = "SELECT ground, over_number, 6*SUM(runs)/SUM(balls) avg_run_rate FROM test.overs GROUP BY ground, over_number;"
# result = execute_read_query(connect, select_query)
# print(result)
# R_df = pd.DataFrame(result, columns=['ground', 'over', 'RR'])
# R_df['RR'] = R_df['RR'].apply(float)
# print(R_df)
#
# ax = sns.lineplot(data=R_df, x='over', y='RR', hue='ground')
# ax.set(xlabel="over", ylabel="run-rate")
#
# ax.legend(title="Ground")
# plt.show()