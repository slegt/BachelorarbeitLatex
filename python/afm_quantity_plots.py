from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
import pandas as pd

from python._states import RC_PARAMS

mpl.use("pgf")
plt.rcParams.update(RC_PARAMS)

path = Path.cwd().parent / 'data' / 'AFM' / 'statistics.csv'
export_path = Path.cwd().parent / 'plots' / 'AFM'
df = pd.read_csv(path)

# plot 1
x_lim_1 = [0, 75]
x_lim_2 = [575, 900]
wspace = 0.03

width_1 = x_lim_1[1] - x_lim_1[0]  # width of the first plot
width_2 = x_lim_2[1] - x_lim_2[0]  # width of the second plot
w = wspace * (width_1 + width_2) / 2  # width of the space between the two plots
midpoint_abs = (width_1 + w + width_2) / 2 - width_1 - w
midpoint_rel = midpoint_abs / width_2

fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True, width_ratios=[width_1, width_2], figsize=(5, 4.4))
fig.subplots_adjust(wspace=wspace)
ax1.set_xlim(x_lim_1[0], x_lim_1[1])
ax2.set_xlim(x_lim_2[0], x_lim_2[1])

ax1.spines.right.set_visible(False)
ax2.spines.left.set_visible(False)
ax2.tick_params(left=False, labelleft=False)

d = .5  # proportion of vertical to horizontal extent of the slanted line
kwargs = dict(marker=[(-d, -1), (d, 1)], markersize=12, linestyle="none", color='k', mec='k', mew=1, clip_on=False)
ax1.plot([1, 1], [0, 1], transform=ax1.transAxes, **kwargs)
ax2.plot([0, 0], [0, 1], transform=ax2.transAxes, **kwargs)

ax1.set_ylabel(r"Rauheit $[\unit{\nano\meter}]$")
ax2.set_xlabel(r"Temperatur $[\unit{\degreeCelsius}]$")
ax2.xaxis.label.set(x=midpoint_rel, y=ax2.xaxis.label.get_position()[1], verticalalignment='top',
                    horizontalalignment='center', transform=mtransforms.blended_transform_factory(ax2.axes.transAxes,
                                                                                                  mtransforms.IdentityTransform()), )
for sample_name in ["W6821-1B", "W6822-1B", "W6823-1B", "W6824-1B"]:
    result_df = df[(df['Sample Name'] == sample_name) & (df['Gas'] == "Sauerstoff")]
    result_df = result_df[['Temperature', 'RMS']]
    result_df = result_df.groupby('Temperature', as_index=False).agg(
        rms_avg=pd.NamedAgg(column='RMS', aggfunc="mean"),
        rms_std=pd.NamedAgg(column='RMS', aggfunc="std"))
    temp = result_df['Temperature'].replace('pre', 25).astype(int).to_numpy()
    roughness_avg = result_df["rms_avg"].to_numpy() * 1e9
    roughness_std = result_df["rms_std"].to_numpy() * 1e9
    ax1.scatter(temp, roughness_avg, label=sample_name)
    ax2.scatter(temp, roughness_avg, label=sample_name)

ax2.legend()
ax1.yaxis.get_major_locator().set_params(integer=True)
plt.savefig(export_path / "sauerstoff.pgf")
print(f"Saved {export_path / 'sauerstoff.pgf'}")

# plot 2
x_lim_1 = [0, 75]
x_lim_2 = [475, 800]
wspace = 0.03

width_1 = x_lim_1[1] - x_lim_1[0]  # width of the first plot
width_2 = x_lim_2[1] - x_lim_2[0]  # width of the second plot
w = wspace * (width_1 + width_2) / 2  # width of the space between the two plots
midpoint_abs = (width_1 + w + width_2) / 2 - width_1 - w
midpoint_rel = midpoint_abs / width_2

fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True, width_ratios=[width_1, width_2], figsize=(5, 4.4))
fig.subplots_adjust(wspace=wspace)
ax1.set_xlim(x_lim_1[0], x_lim_1[1])
ax2.set_xlim(x_lim_2[0], x_lim_2[1])

ax1.spines.right.set_visible(False)
ax2.spines.left.set_visible(False)
ax2.tick_params(left=False, labelleft=False)

d = .5  # proportion of vertical to horizontal extent of the slanted line
kwargs = dict(marker=[(-d, -1), (d, 1)], markersize=12, linestyle="none", color='k', mec='k', mew=1, clip_on=False)
ax1.plot([1, 1], [0, 1], transform=ax1.transAxes, **kwargs)
ax2.plot([0, 0], [0, 1], transform=ax2.transAxes, **kwargs)

ax1.set_ylabel(r"Rauheit $[\unit{\nano\meter}]$")
ax2.set_xlabel(r"Temperatur $[\unit{\degreeCelsius}]$")
ax2.xaxis.label.set(x=midpoint_rel, y=ax2.xaxis.label.get_position()[1], verticalalignment='top',
                    horizontalalignment='center', transform=mtransforms.blended_transform_factory(ax2.axes.transAxes,
                                                                                                  mtransforms.IdentityTransform()), )
for sample_name in ["W6821-1C", "W6822-1C", "W6823-1C", "W6824-1C"]:
    result_df = df[(df['Sample Name'] == sample_name) & (df['Gas'] == "Vakuum")]
    result_df = result_df[['Temperature', 'RMS']]
    result_df = result_df.groupby('Temperature', as_index=False).agg(
        rms_avg=pd.NamedAgg(column='RMS', aggfunc="mean"),
        rms_std=pd.NamedAgg(column='RMS', aggfunc="std"))
    temp = result_df['Temperature'].replace('pre', 25).astype(int).to_numpy()
    roughness_avg = result_df["rms_avg"].to_numpy() * 1e9
    roughness_std = result_df["rms_std"].to_numpy() * 1e9
    ax1.scatter(temp, roughness_avg, label=sample_name)
    ax2.scatter(temp, roughness_avg, label=sample_name)

ax2.legend()
ax1.yaxis.get_major_locator().set_params(integer=True)
# fig.show()
plt.savefig(export_path / "vakuum.pgf")#
print(f"Saved {export_path / 'vakuum.pgf'}")
