import pathlib
import xml.etree.ElementTree as ET

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.transforms as mtransforms
import numpy as np

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


def create_plot(sample_names):
    hspace = 0.1
    cm = mpl.colormaps.get_cmap("tab10")
    if len(sample_names) == 1:
        fig, axes = plt.subplots(len(sample_names), 1, sharex=True,
                                 figsize=(0.98 * LINEWIDTH, 1.6 / 5 * len(sample_names) * LINEWIDTH))
    else:
        fig, axes = plt.subplots(len(sample_names), 1, sharex=True,
                                 figsize=(0.98 * LINEWIDTH, 0.8 / 5 * len(sample_names) * LINEWIDTH))

    fig.subplots_adjust(hspace=hspace, top=0.99)

    if len(sample_names) == 1:
        axes = [axes]
    axes = axes[::-1]



    midpoint = (len(sample_names) * (1 + hspace) - hspace) / 2
    for i, name in enumerate(sample_names):
        path = (pathlib.Path.cwd().parent / 'data' / 'XRD' / 'GIXRD' / f'{name}.xrdml')
        angles, intensities_relative = get_data(path)
        axes[i].plot(angles, intensities_relative, color=cm(i), lw=0.1)
        axes[i].set_yscale("log")
        axes[i].set_xlim(angles[0], angles[-1])
        axes[i].set_yticks([])
        axes[i].get_yaxis().set_major_formatter(ticker.NullFormatter())
        axes[i].get_yaxis().set_minor_formatter(ticker.NullFormatter())

        if "B" in name:
            gas = "Sauer-\nstoff"
        elif "C" in name:
            gas = "Vakuum"
        elif "D" in name:
            gas = "Luft"
        else:
            gas = "Proben-\nhalter"

        axes[i].text(1.01, 0.5, gas, transform=axes[i].transAxes, ha="left", va="center")

    for ax in axes[1:]:
        ax.tick_params(bottom=False)

    axes[0].set_xlabel(r"$2\theta$ [°]")
    axes[0].set_ylabel("I [willk. Einheit]")
    axes[0].yaxis.label.set(
        x=0, y=midpoint,
        verticalalignment='bottom', horizontalalignment='center',
        rotation='vertical', rotation_mode='anchor',
        transform=mtransforms.blended_transform_factory(
            mtransforms.IdentityTransform(), axes[0].yaxis.axes.transAxes),
    )
    export_path = pathlib.Path.cwd().parent / 'plots' / 'XRD' / f'gixrd_{sample_names[0][:5]}.pgf'
    # export_path.parent.mkdir(parents=True, exist_ok=True)
    if len(sample_names) > 1:
        fig.subplots_adjust(right=0.85, left=0.05, bottom=0.18)
    else:
        fig.tight_layout()

    fig.savefig(export_path)
    # print(f"Saved {export_path}")


W6821 = ["sample_holder", "W6821-1B", "W6821-1C", "W6821-1D"]
create_plot(W6821)

W6822 = ["W6822-1B", "W6822-1C", "W6822-1D"]
create_plot(W6822)

W6823 = ["W6823-1D"]
create_plot(W6823)

W6824 = ["W6824-1B", "W6824-1C", "W6824-1D"]
create_plot(W6824)

