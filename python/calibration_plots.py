import pathlib

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

from python._states import RC_PARAMS, LINEWIDTH


# sixth plot


mpl.use("pgf")
plt.rcParams.update(RC_PARAMS)
plt.rcParams.update({"figure.figsize": (LINEWIDTH * 0.49, LINEWIDTH * 0.35),
                     "savefig.bbox": 'tight',
                     "savefig.pad_inches": 0})


A = 3.9083e-3
B = -5.775e-7
delta_A = 0.00005e-3
delta_B = 0.00005e-7
R0 = 1000

def exponential(x, a, b,):
    return a * np.exp(b * x)

def linear(x, m, n):
    return m * x + n


def resistance_to_temp(r):
    T = - A / (2 * B) - np.sqrt((A / (2 * B)) ** 2 + (r * 1000 - R0) / (B * R0))
    return T


def temp_to_resistance(T):
    return R0 * (1 + A * T + B * T ** 2)


def T_real(A, B, m, n, m2, n2, T_pyro):
    T = - A / (2 * B) - np.sqrt((A / (2 * B)) ** 2 + (m * m2 * T_pyro + m * n2 + n - R0) / (B * R0))
    return T


def partial_A(A, B, m, n, m2, n2, T_pyro):
    return (- 1 / (2 * B) - A / (4 * B ** 2) * ((A / (2 * B)) ** 2 + (m * m2 * T_pyro + m * n2 + n - R0) / (B * R0))
            ** (-1 / 2))


def partial_B(A, B, m, n, m2, n2, T_pyro):
    return (A / (2 * B ** 2) + (A ** 2 / (2 * B ** 3) + (m * m2 * T_pyro + m * n2 + n - R0) / (B ** 2 * R0)) *
            ((A / (2 * B)) ** 2 + (m * m2 * T_pyro + m * n2 + n - R0) / (B * R0)) ** (-1 / 2))


def partial_m(A, B, m, n, m2, n2, T_pyro):
    return ((m2 * T_pyro + n2) / (2 * B * R0) *
            ((A / (2 * B)) ** 2 + (m * m2 * T_pyro + m * n2 + n - R0) / (B * R0)) ** (-1 / 2))


def partial_n(A, B, m, n, m2, n2, T_pyro):
    return 1 / (2 * B * R0) * ((A / (2 * B)) ** 2 + (m * m2 * T_pyro + m * n2 + n - R0) / (B * R0)) ** (-1 / 2)


def partial_m2(A, B, m, n, m2, n2, T_pyro):
    return m * T_pyro / (2 * B * R0) * ((A / (2 * B)) ** 2 + (m * m2 * T_pyro + m * n2 + n - R0) / (B * R0)) ** (-1 / 2)


def partial_n2(A, B, m, n, m2, n2, T_pyro):
    return m / (2 * B * R0) * ((A / (2 * B)) ** 2 + (m * m2 * T_pyro + m * n2 + n - R0) / (B * R0)) ** (-1 / 2)


def partial_T_pyro(A, B, m, n, m2, n2, T_pyro):
    return m * m2 / (B * R0) * ((A / (2 * B)) ** 2 + (m * m2 * T_pyro + m * n2 + n - R0) / (B * R0)) ** (-1 / 2)


def delta_T_real(A, B, m, n, m2, n2, T_pyro):
    p = A, B, m, n, m2, n2, T_pyro
    delta_T = np.sqrt(
        (partial_A(*p) * delta_A) ** 2 + (partial_B(*p) * delta_B) ** 2 + (partial_m(*p) * delta_m) ** 2 + (
                partial_n(*p) * delta_n) ** 2 + (partial_m2(*p) * delta_m2) ** 2 + (partial_n2(*p) * delta_n2) ** 2 + (
                partial_T_pyro(*p) * delta_T_pyro) ** 2)
    return delta_T


base_path = pathlib.Path.cwd().parent / 'data' / 'calibration'
base_export_path = pathlib.Path.cwd().parent / 'plots' / 'calibration'

# first and second plot
df1 = pd.read_csv(base_path / 'furnace_calibration.csv')
df1 = df1[df1['t'].notna() & df1['R1'].notna() & df1['R2'].notna()]
t = df1["t"].to_numpy()
index = np.where(t > 45000)[0][0]
t = t[:index] / 3600
r_lit = df1["R1"].to_numpy()[:index] / 1000
r_pt = df1["R2"].to_numpy()[:index] / 1000
(m, n), cov = curve_fit(linear, r_lit, r_pt)

plt.scatter(t[::10], r_lit[::10], label=r"$R_{\text{Lit}}$")
plt.scatter(t[::10], r_pt[::10], label=r"$R_{\text{Pt}}$")
plt.xlabel(r"$t \text{ in }  \unit{\hour} $")
plt.ylabel(r"$R \text{ in } \unit{\kilo\ohm} $")
plt.legend()
export_path = base_export_path / "furnace_calibration_1.pgf"
export_path.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(export_path)
print(f"Saved {export_path}")
plt.close()

plt.scatter(r_lit[::10], r_pt[::10], zorder=1, label="Messwerte")
plt.plot(r_lit, linear(r_lit, m, n), color="red", zorder=2, label="Fit")
plt.xlabel(r"$R_{\text{Lit}} \text{ in } \unit{\kilo\ohm}$")
plt.ylabel(r"$R_{\text{Pt}} \text{ in } \unit{\kilo\ohm}$")
plt.legend()
export_path = base_export_path / "furnace_calibration_2.pgf"
export_path.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(export_path)
print(f"Saved {export_path}")
plt.close()

# third plot
df = pd.read_csv(base_path / 'a_chamber_calibration.csv')
r1 = df["r1"].to_numpy()
r2 = df["r2"].to_numpy()
t_pyro_1 = df["t_pyro_1"].to_numpy()
t_pyro_2 = df["t_pyro_2"].to_numpy()
r2 = r2[~np.isnan(r2)]
t_pyro_2 = t_pyro_2[~np.isnan(t_pyro_2)]

r_lit_to_r_pt = lambda r: linear(r, m, n)
t_exp_1 = resistance_to_temp(r_lit_to_r_pt(r1))
t_exp_2 = resistance_to_temp(r_lit_to_r_pt(r2))
(m2, n2), cov2 = curve_fit(linear, np.concatenate((t_pyro_1, t_pyro_2)), np.concatenate((r1, r2)))

plt.scatter(t_pyro_1, r1, label=r"$\text{aufwärts}$")
plt.scatter(t_pyro_2, r2, label=r"$\text{abwärts}$")
plt.plot(t_pyro_1, linear(t_pyro_1, m2, n2), label=r"$\text{Fit}$", color="orange")
plt.xlabel(r"$T \text{ in } \unit{\degreeCelsius}$")
plt.ylabel(r"$R \text{ in } \unit{\kilo\ohm}$")
plt.legend()
export_path = base_export_path / "a_chamber_calibration.pgf"
export_path.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(export_path)
print(f"Saved {export_path}")
plt.close()

# fourth plot
delta_m = cov[0, 0] ** 0.5
delta_n = cov[1, 1] ** 0.5 * 1000
delta_m2 = cov2[0, 0] ** 0.5 * 1000
delta_n2 = cov2[1, 1] ** 0.5 * 1000
R0 = 1000
delta_T_pyro = 1
T_pyro = np.linspace(400, 600, 1000)

# *1000 for kOhm to Ohm
T = T_real(A, B, m, n * 1000, m2 * 1000, n2 * 1000, T_pyro)
dT = delta_T_real(A, B, m, n * 1000, m2 * 1000, n2 * 1000, T_pyro)

plt.plot(T_pyro, T, label=r"$T_{\text{real}}$")
plt.fill_between(T_pyro, T - dT, T + dT, alpha=0.5, color="orange", label=r"$\Delta T$")
plt.xlabel(r"$T_{\text{Pyro}} \text{ in } \unit{\degreeCelsius}$")
plt.ylabel(r"$T_{\text{real}} \text{ in } \unit{\degreeCelsius}$")
plt.legend()
export_path = base_export_path / "final_calibration.pgf"
export_path.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(export_path)
print(f"Saved {export_path}")
plt.close()

# fifth plot
df = pd.read_csv(base_path / "quenching_time.csv", sep=',')
df = df[df['t'].notna()]
df = df[df["R"].notna()]
t_q = df["t"].to_numpy()
R_q = df["R"].to_numpy()

plt.plot(t_q / 60 - 74, R_q / 1000)
plt.xlabel(r"$t \text{ in } \unit{\minute}$")
plt.ylabel(r"$R \text{ in } \unit{\kilo\ohm}$")
plt.text(2.1, 4.877, r"$T\simeq\qty{350}{\degreeCelsius}$", ha="left", va="top")
plt.text(5.8, 3.52, r"$T\simeq\qty{25}{\degreeCelsius}$", ha="right", va="bottom")
plt.ylim(3, 5)
plt.xlim(0, 6)
plt.savefig(base_export_path / "quenching_time.pgf")
plt.close()

min, max = np.where(t_q > 74 * 60)[0][0], np.where(t_q > 80 * 60)[0][0]
print(min, max)
t_q = t_q[min:max]
print(R_q[min:max])
print(t_q)



df = pd.read_csv(base_path / "furnace_heating_rate.csv", sep=',')
t = df["t"].to_numpy()
T = df["T"].to_numpy()

plt.plot(t, T)
plt.xlabel(r"$t \text{ in } \unit{\minute} $")
plt.ylabel(r"$T \text{ in } \unit{\degreeCelsius}$")
plt.savefig(base_export_path / "furnace_heating_rate.pgf")
plt.close()

print("Parameter für Fit 1")
print(f"m = {m} +- {delta_m}")
print(f"n = {n} +- {delta_n/1000}") # /1000 for Ohm to kOhm
print("Parameter für Fit 2")
print(f"m = {m2} +- {delta_m2/1000}")
print(f"n = {n2} +- {delta_n2/1000}")