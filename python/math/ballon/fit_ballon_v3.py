import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas.plotting import table
from scipy.optimize import curve_fit

# Load your data from the CSV file
data = pd.read_csv("./Ballon_data_opg6.csv")  # file for data as comma seperated values
print(data.head(10))
# name x and y values from the data correlate that with the values
x_data = data["Rumfang (cm³)"].values
y_data = data["Tryk i ballon (Pa)"].values

# fig, ax = plt.subplots(figsize=(8, 4))
# ax.axis("off")
# table_data = table(
#     ax, data.head(5), loc="center", colWidths=[0.55] * len(data.head(5).columns)
# )

# Save the plot as an image (e.g., PNG)
# plt.savefig("table_image.png", bbox_inches="tight")


# Initial Plot
# plt.figure(figsize=(16, 12))
# plt.scatter(x_data, y_data, label="Data")
# plt.xlabel("Rumfang", fontsize=17)
# plt.ylabel("Tryk", fontsize=17)
# plt.title("Temperature vs Energy", fontsize=22)
# plt.show()


# def function(x, a, b, c, d):
#     return a * (x - b) / (x**3 - c) + d
# def function(x, a, b, c):
# return (
# a
# * (x ** (-1 / 3) - x ** (-7 / 3))
# * (
# (x ** (2 / 3) + x ** (-4 / 3) - 9 * b)
# / (x ** (2 / 3) + x ** (-4 / 3) - 3 * b)
# )
#        + c
#    )


def function(x, a, b, c):
    x = np.asarray(x, dtype=float)
    eps_x = 1e-12
    eps_d = 1e-9

    # avoid x <= 0 for negative powers
    x = np.clip(x, eps_x, None)

    num = x ** (-1 / 3) - x ** (-7 / 3)
    d_top = x ** (2 / 3) + x ** (-4 / 3) - 9 * b
    d_bot = x ** (2 / 3) + x ** (-4 / 3) - 3 * b

    # avoid divide by zero in the rational factor
    d_bot = np.where(np.abs(d_bot) < eps_d, np.sign(d_bot) * eps_d, d_bot)

    return a * num * (d_top / d_bot) + c


# Fit the data to the tanh function
# Set initial guess to apparent inflection point
initial_guess = [6486.0, 248.0, 100260.0]
# params, covariance = curve_fit(function, x_data, y_data, p0=initial_guess)

bounds = (
    [-1e6, 1e-6, 9.0e4],  # a_min, b_min, c_min
    [1e6, 1e6, 1.2e5],  # a_max, b_max, c_max
)

mask = np.isfinite(x_data) & np.isfinite(y_data) & (x_data > 0)
x_fitdata = x_data[mask]
y_fitdata = y_data[mask]

params, cov = curve_fit(
    function,
    x_fitdata,
    y_fitdata,
    p0=initial_guess,
    bounds=bounds,
    method="trf",
    loss="soft_l1",
    f_scale=1.0,
    maxfev=100000,
)
# Extract the parameters
a, b, c = params
print(params)

# Create a range of x values for the curve change value of "127" to max number or data points i didnt know how to get max size of the data sheet
x_fit = np.linspace(min(x_data), max(x_data), 137)
# Calculate the y values for the fitted curve
y_fit = function(x_fit, a, b, c)

plt.figure(figsize=(16, 12))
plt.scatter(x_data, y_data, label="Data")
plt.plot(x_fit, y_fit, label="Tanh Fit", color="red")
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.xlabel("Temperature", fontsize=17)
plt.ylabel("Energy", fontsize=17)
plt.title("Temperature vs Energy", fontsize=22)
# Display the equation
equation = f"y = {a:.2f} * (x ** (-1/3) - x ** (-7/3)) * ((x ** (2/3) + x ** (-4/3) - 9 * {b:.2f})/(x ** (2/3) + x ** (-4/3) - 3 * {b:.2f})) + {c:.2f}"
print("Equation:", equation)


text_x = 8  # x-coordinate
text_y = 16  # y-coordinate

plt.text(
    text_x,
    text_y,
    equation,
    fontsize=19,
    color="red",
    bbox={"facecolor": "white", "alpha": 0.7, "edgecolor": "gray"},
)
plt.show()
