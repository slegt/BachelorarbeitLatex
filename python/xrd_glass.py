import pathlib
import xml.etree.ElementTree as ET

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from numpy import log

from python._states import LINEWIDTH

mpl.use("pgf")
plt.rcParams.update({
    "font.size": 12,
    "font.family": "serif",
    "font.serif": [],
})


def get_data(path):
    ns = {'': 'http://www.xrdml.com/XRDMeasurement/2.1'}
    tree = ET.parse(path)
    root = tree.getroot()
    counts = root.find(".//counts", ns).text
    start_position = float(root.find(".//startPosition", ns).text)
    end_position = float(root.find(".//endPosition", ns).text)

    intensities = np.array([int(num) for num in counts.split()])
    intensities_relative = intensities / np.max(intensities) * 100
    angles = np.linspace(start_position, end_position, len(intensities))
    return angles, intensities_relative


path = pathlib.Path.cwd().parent / 'data' / 'XRD' / '_misc' / 'glass.xrdml'
plt.rcParams["figure.figsize"] = (LINEWIDTH * 0.98, LINEWIDTH / 3)
angles, intensities_relative = get_data(path)

plt.plot(angles, log(intensities_relative), zorder=1, lw=0.1)
plt.axvline(x=44.3280, ymin=0, ymax=log(100), alpha=0.25, color="gray", linestyle="--", zorder=100)
plt.axvline(x=64.6551, ymin=0, ymax=log(100), alpha=0.25, color="gray", linestyle="--")
plt.axvline(x=81.9637, ymin=0, ymax=log(100), alpha=0.25, color="gray", linestyle="--")
plt.axvline(x=98.6066, ymin=0, ymax=log(100), alpha=0.25, color="gray", linestyle="--")
plt.axvline(x=115.8937, ymin=0, ymax=log(100), alpha=0.25, color="gray", linestyle="--")
plt.yticks([])

plt.xlim(angles[0], angles[-1])
plt.xlabel(r"$2\theta$ [°]")
plt.ylabel("I [willk. E.]")
plt.tight_layout()

export_path = pathlib.Path.cwd().parent / 'plots' / 'XRD' / 'glass.pgf'
plt.savefig(export_path)