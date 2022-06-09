import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from pmdarima import auto_arima
# Ignore harmless warnings
import warnings
from statsmodels.tsa.statespace.sarimax import SARIMAX

warnings.filterwarnings("ignore")

file = 'Moscow.csv'
d_f = pd.read_csv(file)

data = dict()
data['Date'] = list()
data['AvgTemperature'] = list()
prev_temp = 0
for i in range(len(d_f)):
    year = str(d_f["Year"][i])
    month = str(d_f["Month"][i])
    day = str(d_f["Day"][i])

    temp = d_f["AvgTemperature"][i]

    if temp > -20:

        data['Date'].append(f'{year}-{month}-{day}')
        data['AvgTemperature'].append(temp)
        prev_temp = temp
    else:
        data['Date'].append(f'{year}-{month}-{day}')
        data['AvgTemperature'].append(prev_temp)

df = pd.DataFrame.from_dict(data)

df.set_index('Date', inplace=True)

# result = seasonal_decompose(df['AvgTemperature'], model='additive', extrapolate_trend='freq', period=365)


# ETS plot
# result.plot()
# plt.show()

#stepwise_fit = auto_arima(df['AvgTemperature'], start_p=1, start_q=1,
#                          max_p=3, max_q=3, m=12,
#                          start_P=0, seasonal=True,
#                         d=None, D=1, trace=True,
#                          error_action='ignore',  # we don't want to know if an order does not work
#                          suppress_warnings=True,  # we don't want convergence warnings
#                          stepwise=True)
# To print the summary
#stepwise_fit.summary()



# Split data into train / test sets
# Train the model on the full dataset
model = SARIMAX(df['AvgTemperature'],
                        order=(2, 0, 2),
                        seasonal_order=(2, 1, 0, 12))
result = model.fit()

# Forecast for the next 3 years
forecast = result.predict(start=len(df)-100,
                          end=(len(df) - 1) + 20 * 12,
                          typ='levels').rename('Forecast')

# Plot the forecast values

fig, ax = plt.subplots(1,1, figsize = (15, 6))

pred_data = dict()
for i in forecast.to_dict():
    pred_data[str(i)[:10]] = forecast.to_dict()[i]


ax.plot(df)
ax.plot(pred_data.keys(), pred_data.values())
#df['AvgTemperature'].plot(figsize=(12, 5), legend=True)
#forecast.plot(legend=True)
plt.show()