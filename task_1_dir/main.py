# Importing required libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from pmdarima import auto_arima

# Ignore harmless warnings
import warnings
from statsmodels.tsa.statespace.sarimax import SARIMAX

warnings.filterwarnings("ignore")

# Read the AirPassengers dataset
df = pd.read_csv('out.csv',
                 index_col='Date')
                 #parse_dates=True,
                 #)
print(df)

stable_data = df.query("Date <= 1100")

#stable_data['Value'].plot(figsize=(12, 5), legend=True)
plt.show()

'''
stepwise_fit = auto_arima(stable_data['Value'], start_p=1, start_q=1,
                          max_p=3, max_q=3, m=12,
                          start_P=0, seasonal=True,
                          d=None, D=1, trace=True,
                          error_action='ignore',  # we don't want to know if an order does not work
                          suppress_warnings=True,  # we don't want convergence warnings
                          stepwise=True)  # set to stepwise

# To print the summary

stepwise_fit.summary()
'''
'''
# Split data into train / test sets
train = stable_data.iloc[:len(stable_data) - 12 * 31]
test = stable_data.iloc[len(stable_data) - 12 * 31:]  # set one year(12 months) for testing

model = SARIMAX(test['Value'],
                order=(1, 0, 0),
                seasonal_order=(2, 1, 0, 12))

result = model.fit()

start = '2021-01-26'
end = '2022-01-01'

# Predictions for one-year against the test set
predictions = result.predict(start=start,
                             end=end,
                             typ='levels').rename("Predictions")

# plot predictions and actual values
predictions.plot(legend=True)
test['Value'].plot(legend=True)

plt.show()
'''

# Train the model on the full dataset
model = SARIMAX(stable_data['Value'],
                order=(1, 0, 0),
                seasonal_order=(2, 1, 0, 12))
result = model.fit()

# Forecast for the next 3 years
forecast = result.predict(start = len(stable_data) - 10 * 12,
                          end = len(df),
                          typ = 'levels').rename('Forecast')

print(forecast)
# Plot the forecast values
df['Value'].plot(figsize=(12, 5), legend=True)
forecast.plot(legend=True)
plt.show()
