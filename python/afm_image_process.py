import csv
import os
import sys

import gwy

settings = gwy.gwy_app_settings_get()
settings['/module/linematch/direction'] = int(gwy.ORIENTATION_HORIZONTAL)
settings['/module/linematch/do_extract'] = False
settings['/module/linematch/do_plot'] = False
settings['/module/linematch/method'] = 0
settings['/module/linematch/max_degree'] = 2
settings['/module/linematch/trim_fraction'] = 0.05
settings['/module/linematch/masking'] = 2


def process_tiff(src_path, dest_path):
    # get container, data_field  and settings
    container = gwy.gwy_app_file_load(src_path)
    # get Topography channel and set fokus
    topo_id = gwy.gwy_app_data_browser_find_data_by_title(container, 'Topography')[0]
    topo_field = container[gwy.gwy_app_get_data_key_for_id(topo_id)]
    gwy.gwy_app_data_browser_select_data_field(container, topo_id)

    # execute transformations
    gwy.gwy_process_func_run("align_rows", container, gwy.RUN_IMMEDIATE)
    gwy.gwy_process_func_run("scars_remove", container, gwy.RUN_IMMEDIATE)
    gwy.gwy_process_func_run("fix_zero", container, gwy.RUN_IMMEDIATE)
    container["/0/base/palette"] = "Gwyddion.net"

    # save file
    dest_path = dest_path.rsplit(".", 1)[0] + ".pdf"
    gwy.gwy_file_save(container, dest_path, gwy.RUN_NONINTERACTIVE)

    # return metadata and statistics
    filename = dest_path.rsplit("/", 1)[-1].rsplit(".", 1)[0]
    sample_name, substrate, gas, temp, type, index = filename.split("_")
    avg, ra, rms, skew, kurtosis = topo_field.get_stats()

    return [sample_name, substrate, gas, temp, type, index, avg, ra, rms, skew, kurtosis]


def replicate_folder_structure(src_path, dest_path, rows):
    for item in os.listdir(src_path):
        if str(item).startswith('_'):
            continue

        src_item = os.path.join(src_path, item)
        dest_item = os.path.join(dest_path, item)

        if os.path.isdir(src_item):
            if not os.path.exists(dest_item):
                os.makedirs(dest_item)
            replicate_folder_structure(src_item, dest_item, rows)
        else:
            if "Topography" in str(src_item):
                rows.append(process_tiff(src_item, dest_item))
                print("File " + str(src_item) + " converted")
    return rows


src_dir = "./data/AFM"
dest_dir = "./plots/AFM"

rows = replicate_folder_structure(src_dir, dest_dir, [])

with open(src_dir + "/statistics.csv", 'wb') as file:
    writer = csv.writer(file)
    writer.writerow(["Sample Name", "Substrate", "Gas", "Temperature", "Type", "Index", "Average", "Ra", "RMS", "Skew",
                     "Kurtosis"])
    for row in rows:
        writer.writerow(row)
