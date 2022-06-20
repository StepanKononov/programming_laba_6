import matplotlib.pyplot as plt
from datetime import datetime
from data_reader import get_data
import numpy as np


def ar_processing(data, dates):
    r = get_r_param(data)
    c = get_c_param(data)
    f_value = []
    print(c, r)
    for i in data:
        f_value.append(c + r * i)
    show_plot(0, len(data), dates, data, f_value, size=(8, 8))
    show_plot(len(data) - 10, len(data), dates, data, f_value, size=(8, 8))


def show_plot(start, stop, dates, data, forecast, size):
    fig, ax = plt.subplots(figsize=size)
    ax.set_title('Курс доллара к рублю')
    ax.plot(dates[start:stop], data[start:stop], label='Реальные значения')
    ax.plot(dates[start:stop], forecast[start:stop], label='Полученные значения')
    legend = ax.legend(loc='best', shadow=True, fontsize='x-large')
    plt.xticks(rotation=45)
    plt.show()


def get_r_param(data):
    mul, sum1, sum2 = 0, 0, 0
    mean1 = sum(data[1:]) / len(data[1:])
    mean2 = sum(data[:-1]) / len(data[:-1])
    for i in range(1, len(data)):
        sum1 += (data[i] - mean1) ** 2
        sum2 += (data[i - 1] - mean2) ** 2
        mul += (data[i] - mean1) * (data[i - 1] - mean2)
    return mul / (sum1 * sum2) ** 0.5


def get_c_param(X):
    numerator = np.cov(X)
    denominator = np.var(X)
    return numerator / denominator


def google_get_data():
    df = get_data().to_dict()
    dates = list()
    y = list()
    for elem in df["Value"]:
        dates.append(datetime.strptime(elem, '%d.%m.%Y'))
        y.append(df["Value"][elem])
    ar_processing(y, dates)


google_get_data()
