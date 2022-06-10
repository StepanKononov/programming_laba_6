# Importing required libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

# Read the AirPassengers dataset
airline = pd.read_csv('task_1_dir/AirPassengers.csv',
					  index_col ='Month',
					  parse_dates = True)

# Print the first five rows of the dataset
airline.head()

# ETS Decomposition
result = seasonal_decompose(airline['Passengers'],
							model ='multiplicative')

# ETS plot
result.plot()
plt.show()


from pmdarima import auto_arima

# Ignore harmless warnings
import warnings

warnings.filterwarnings("ignore")

# Fit auto_arima function to AirPassengers dataset
stepwise_fit = auto_arima(airline['Passengers'], start_p=1, start_q=1,
						  max_p=3, max_q=3, m=12,
						  start_P=0, seasonal=True,
						  d=None, D=1, trace=True,
						  error_action='ignore',  # we don't want to know if an order does not work
						  suppress_warnings=True,  # we don't want convergence warnings
						  stepwise=True)  # set to stepwise

# To print the summary
stepwise_fit.summary()

train = airline.iloc[:len(airline) - 12]
test = airline.iloc[len(airline) - 12:]  # set one year(12 months) for testing

# Fit a SARIMAX(0, 1, 1)x(2, 1, 1, 12) on the training set
from statsmodels.tsa.statespace.sarimax import SARIMAX

model = SARIMAX(train['Passengers'],
				order=(0, 1, 1),
				seasonal_order=(2, 1, 1, 12))

result = model.fit()
result.summary()