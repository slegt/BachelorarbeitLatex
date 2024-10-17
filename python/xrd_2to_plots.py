import colorsys
import pathlib
import xml.etree.ElementTree as ET

import matplotlib as mpl
import matplotlib.colors as mc
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.transforms as mtransforms
import numpy as np

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


def adjust_lightness(color, amount=0.5):
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1])), c[2])


def create_plot(gas, temperature_array, sample_name):
    hspace = 0.1
    cm = mpl.colormaps.get_cmap("tab10")
    fig, axes = plt.subplots(len(temperature_array), 1, sharex=True, figsize=(5, 4.4))
    fig.subplots_adjust(hspace=hspace)
    axes = axes[::-1]

    midpoint = (len(temperature_array) * (1 + hspace) - hspace) / 2
    for i, temperature in enumerate(temperature_array):
        path = (pathlib.Path.cwd().parent / 'data' / 'XRD' / ('XG-' + gas) / ('XG-' + temperature)
                / f'{sample_name}_XG_{gas}_{temperature}.xrdml')
        angles, intensities_relative = get_data(path)
        angles, intensities_relative = angles[::10], intensities_relative[::10]
        axes[i].plot(angles, intensities_relative, color=cm(i))
        axes[i].set_yscale("log")
        axes[i].set_xlim(angles[0], angles[-1])
        axes[i].set_ylim(25, 100)
        axes[i].set_yticks([40, 100])
        axes[i].get_yaxis().set_major_formatter(ticker.ScalarFormatter())
        axes[i].get_yaxis().set_minor_formatter(ticker.NullFormatter())

        temperature = "25" if temperature == "pre" else temperature
        axes[i].text(1.01, 0.5, f"{temperature} °C", transform=axes[i].transAxes, ha="left", va="center")

    for ax in axes[1:]:
        ax.tick_params(bottom=False)

    axes[0].set_xlabel(r"$2\theta$ [°]")
    axes[0].set_ylabel("Intensität [arb. u.]")
    axes[0].yaxis.label.set(
        x=0, y=midpoint,
        verticalalignment='bottom', horizontalalignment='center',
        rotation='vertical', rotation_mode='anchor',
        transform=mtransforms.blended_transform_factory(
            mtransforms.IdentityTransform(), axes[0].yaxis.axes.transAxes),
    )
    export_path = pathlib.Path.cwd().parent / 'plots' / 'XRD' / f'{sample_name}_{gas}.pgf'
    export_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(export_path)
    print(f"Saved {export_path}")


sauerstoff_samples = ["W6821-1B", "W6822-1B", "W6823-1B", "W6824-1B"]
sauerstoff_temperature_array = ["pre", "600", "700", "750", "800", "875"]

for sample in sauerstoff_samples:
    create_plot("Sauerstoff", sauerstoff_temperature_array, sample)

vakuum_samples = ["W6821-1C", "W6822-1C", "W6823-1C", "W6824-1C"]
vakuum_temperature_array = ["pre", "500", "600", "700", "750"]

for sample in vakuum_samples:
    create_plot("Vakuum", vakuum_temperature_array, sample)