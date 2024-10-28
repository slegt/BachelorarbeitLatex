import pathlib

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from numpy import log

from python._states import LINEWIDTH, RC_PARAMS

mpl.use("pgf")
plt.rcParams.update(RC_PARAMS)
plt.rcParams["figure.figsize"] = (LINEWIDTH * 0.7, LINEWIDTH * 0.5)

export_path = pathlib.Path.cwd().parent / "plots" / "theory"
export_path.mkdir(parents=True, exist_ok=True)


def mixing_entropy(x, N):
    return -(x * log(x) + (1 - x) * log((1 - x) / (N - 1)))


x = np.linspace(0.001, 0.999, 100)
for i in range(2, 6):
    plt.plot(x, mixing_entropy(x, i), label=f"$N = {i}$")
    plt.vlines(1 / i, ymin=0, ymax=mixing_entropy(1 / i, i), linestyle="dashed", colors="gray")
    plt.scatter(1 / i, mixing_entropy(1 / i, i), zorder=10)

plt.xlabel(r"$x$")
plt.ylabel(r"$S_{\text{Misch}} / \mathrm{R}$")
plt.xlim(0, 1)
plt.ylim(0, 1.65)
plt.legend()
plt.tight_layout()
plt.savefig(export_path / "mixing_entropy.pgf", bbox_inches="tight", pad_inches=0)
plt.close()


def mixing_enthalpy(x, a):
    return a * x * (1 - x)


def mixing_entropy(x):
    return -(x * log(x) + (1 - x) * log(1 - x))


def mixing_gibbs_energy(x, T):
    return mixing_enthalpy(x, 1) - T * mixing_entropy(x)


x = np.linspace(0.001, 0.999, 100)
fig, axes = plt.subplots(1, 3, figsize=(LINEWIDTH, LINEWIDTH * 0.5))
axes[0].plot(x, mixing_enthalpy(x, 1), label=r"$a > 0$")
axes[0].plot(x, mixing_enthalpy(x, -1), label=r"$a < 0$")
axes[0].set_xlabel(r"$x$")
axes[0].set_ylabel(r"$\Delta H_{\text{Misch}}$")
axes[0].set_xlim(0, 1)
axes[0].legend()
axes[0].set_yticks([0])
axes[0].set_xticks([0, 0.5, 1])

axes[1].plot(x, mixing_entropy(x), label=r"$S_{\text{Misch}}$")
axes[1].set_xlabel(r"$x$")
axes[1].set_ylabel(r"$S_{\text{Misch}}$")
axes[1].set_xlim(0, 1)
axes[1].set_yticks([0])
axes[1].set_xticks([0, 0.5, 1])

for i, T in enumerate([0.01, 0.05, 0.1, 0.3, 0.5, 0.7, 1]):
    # Rotton wird mit zunehmendem Index intensiver
    red_intensity = 0.3 + 0.7 * (i / 7)
    color = (red_intensity, 0.1, 0.1)  # RGB-Farbwert
    axes[2].plot(x, mixing_gibbs_energy(x, T), label=f"$T = {T}$", color=color)
    axes[2].arrow(0.5, 0.2, 0, -0.5, head_width=0.05, head_length=0.02, fc='k', ec='k', color="black")
    axes[2].text(0.6, -0.15, "$T$", ha="left", va="center", color="black")
axes[2].set_yticks([0])
axes[2].set_xlabel(r"$x$")
axes[2].set_ylabel(r"$\Delta G_{\text{Misch}}$")
axes[2].set_xticks([0, 0.5, 1])

fig.tight_layout()
fig.savefig(export_path / "mixing_properties.pgf", bbox_inches="tight", pad_inches=0)
