import numpy as np
from scipy.optimize import fsolve


misch1 = np.array([17.62, 19.08, 20.06, 22.52, 20.72]) / 100
misch2 = np.array([16.5, 19.01, 20.04, 23.29, 21.16]) / 100
misch3 = np.array([16.13, 19.56, 20.79, 22.66, 20.86]) / 100
misch4 = np.array([15.03, 20.93, 21.32, 21.61, 21.12]) / 100


def function(x, misch):
    return np.sum(misch * np.log(misch)) - x * np.log(x) - (1 - x) * np.log((1 - x) / 4)


for i, name in zip([misch1, misch2, misch3, misch4], ["W6823", "W6821", "W6822", "W6824"]):
    print(name)
    f_solve_function = lambda x: function(x, i)
    print(fsolve(f_solve_function, 0.15))
