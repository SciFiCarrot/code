import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas.plotting import table
from scipy.optimize import curve_fit

# Load your data from the CSV file
data = pd.read_csv("./Brydningsdata.csv")  # file for data as comma seperated values
print(data.head(10))
# name x and y values from the data correlate that with the values
x_data = data["Sin(i)"].values
y_data = data["Sin(b)"].values


def function(x, a, b):
    return a * x + b


initial_guess = [1, 0]

mask = np.isfinite(x_data) & np.isfinite(y_data) & (x_data > 0)
x_fitdata = x_data[mask]
y_fitdata = y_data[mask]

params, cov = curve_fit(
    function,
    x_fitdata,
    y_fitdata,
    p0=initial_guess,
)
# Extract the parameters
a, b = params
print(params)

# print(params[0] + "x + " + params[1])
