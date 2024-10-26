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
            splitted_name = item.rsplit("_", 4)
            default = "_".join(splitted_name[1:])
            custom = splitted_name[0]

            sample_name = custom[0:8]


            substrate_gas = src_path.rsplit("/", 3)[-3]
            substrate, gas = substrate_gas.split("-")
            print(sample_name[7], substrate_gas)
            if gas == "Vakuum" and sample_name[7] == "B":
                sample_name = sample_name[0:-1] + "C"

            temp = src_path.rsplit("/", 2)[-2].split("-")[1]
            ending = "." + default.rsplit(".", 1)[-1]
            if "Topography" in str(src_item):
                type = "Topography"
            elif "Error" in str(src_item):
                type = "Error"
            elif "Lateral" in str(src_item):
                type = "Lateral"
            else:
                type = "Unknown"

            print(sample_name, substrate, gas, temp, type, default)
            for i in range(1, 5):
                new_name = "_".join([sample_name, substrate, gas, temp, type, str(i)]) + ending
                dest_item = os.path.join(dest_path, new_name)
                if not os.path.isfile(dest_item):
                    shutil.copy(src_item, dest_item)
                    break


src_dir = "../data2/AFM"
dest_dir = "../data_renamed/AFM"
replicate_folder_structure(src_dir, dest_dir)
