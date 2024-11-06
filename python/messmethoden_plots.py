import pathlib

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from numpy import log

from python._states import LINEWIDTH, RC_PARAMS

mpl.use("pgf")
plt.rcParams.update(RC_PARAMS)
plt.rcParams["figure.figsize"] = (LINEWIDTH * 0.6, LINEWIDTH * 0.4)

export_path = pathlib.Path.cwd().parent / "plots" / "messmethoden"
export_path.mkdir(parents=True, exist_ok=True)


def lennard_jones_potential(r):
    return 4 * (1/r**12 - 1/r**6)

min = 2**(1/6)
x = np.linspace(min, 3, 60)
x2 = np.linspace(0.95, min, 80)
plt.plot(x, lennard_jones_potential(x))
plt.plot(x2, lennard_jones_potential(x2))
plt.hlines(0, xmin=0, xmax=3, linestyle="dashed", colors="gray")
plt.hlines(-1, xmin=0, xmax=3, linestyle="dashed", colors="gray")
plt.xlim(0.5, 3)
plt.xlabel(r"$r / \mathrm{R_a}$")
plt.ylabel(r"$U_{\text{LJ}} / \mathrm{U_0}$")
plt.tight_layout()
plt.savefig(export_path / "lennard_jones_potential.pgf")

