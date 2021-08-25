import pandas as pd
from SQL_functions import execute_read_query
from SQL_functions import create_connection
from credentials import credentials
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# get credentials and connect to a MySQL database
HOST, USER, PASSWORD, DB_NAME = credentials()
connector = create_connection(HOST, USER, PASSWORD, DB_NAME)

# simple test to display 10 rows from the database
select_query = "SELECT season, over_number, ball_number, score, wicket, wicket_num FROM balls;"
results = execute_read_query(connector, select_query)

w_DF = pd.DataFrame(results, columns=['season', 'over', 'ball', 'score', 'wicket', 'num_wickets'])

print(w_DF.head())

w_DF['over'] = w_DF['over']/20
w_DF['ball'] = w_DF['ball']/6
w_DF['score'] = w_DF['score']/300
w_DF['num_wickets'] = w_DF['num_wickets']/10

print(w_DF.head())

test_data = w_DF[w_DF['season'] == 10]
train_data = w_DF[w_DF['season'] != 10]

print(test_data.head())
print(train_data.head())

inputs_test = test_data.iloc[:, [1, 2, 3, 5]].to_numpy()
outputs_test = test_data.iloc[:, 4].to_numpy()
inputs_train = train_data.iloc[:, [1, 2, 3, 5]].to_numpy()
outputs_train = train_data.iloc[:, 4].to_numpy()

print(inputs_test)

model = Sequential([
  Dense(4, activation='relu', input_shape=(4,)),
  Dense(16, activation='relu'),
  Dense(16, activation='relu'),
  Dense(4, activation='relu'),
  Dense(1, activation='softmax'),
])

model.compile(
  optimizer='adam',
  loss='binary_crossentropy',
  metrics=['BinaryAccuracy'],
)

model.fit(x=inputs_train, y=outputs_train, epochs=100,
          validation_data=(inputs_test, outputs_test))
