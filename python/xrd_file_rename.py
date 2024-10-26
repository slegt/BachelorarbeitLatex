import os
import shutil


def replicate_folder_structure(src_path, dest_path):
    for item in os.listdir(src_path):
        if str(item).startswith('_'):
            continue

        src_item = os.path.join(src_path, item)
        dest_item = os.path.join(dest_path, item)

        if os.path.isdir(src_item):
            if not os.path.exists(dest_item):
                os.makedirs(dest_item)
            replicate_folder_structure(src_item, dest_item)
        else:
            sample_name, default = item.split("_", 1)
            if len(sample_name) != 8:
                sample_name, default = item.split("@", 1)
            if len(sample_name) != 8:
               print("Error converting " + (os.path.join(src_path, item)))
               continue
            substrate_gas = src_path.rsplit("/", 2)[-2]
            substrate, gas = substrate_gas.split("-")
            print(sample_name[7], substrate_gas)

            temp = src_path.rsplit("/", 1)[-1].split("-")[1]
            ending = "." + default.rsplit(".", 1)[-1]

            new_name = "_".join([sample_name, substrate, gas, temp]) + ending
            dest_item = os.path.join(dest_path, new_name)
            shutil.copy(src_item, dest_item)



src_dir = "../data2/XRD"
dest_dir = "../data_renamed/XRD"
replicate_folder_structure(src_dir, dest_dir)
