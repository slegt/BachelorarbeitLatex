import numpy as np
import xml.etree.ElementTree as ET
import pathlib
import matplotlib.pyplot as plt

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


path = pathlib.Path.cwd().parent / 'data' / 'XRD' / '_misc' / 'sampleholder.xrdml'

angles, intensities_relative = get_data(path)
plt.plot(angles, intensities_relative)
plt.xlim(angles[0], angles[-1])
plt.xlabel(r"$2\theta$ [°]")
plt.ylabel(r"$I / I_\mathrm{max}$ [%]")
plt.show()