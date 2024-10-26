import os
import pathlib

from PIL import Image

base_src_path = pathlib.Path.cwd().parent / "data" / "EDX"
base_dest_path = pathlib.Path.cwd().parent / "plots" / "EDX"

for sample_name in ["W6821-3D", "W6822-3D", "W6823-3D", "W6824-3D"]:
    src_path = base_src_path / sample_name
    dest_path = base_dest_path / sample_name

    for file in os.listdir(src_path):
        if os.path.isdir(src_path / file):
            continue

        image = Image.open(src_path / file)
        name = file.rsplit(".", 1)[0]

        if name == "map":
            box_position_y = 884
            bottom_rows = image.crop((0, 884, image.width, image.height))
            new_image = Image.new("RGB", (image.width, image.height - 47))
            new_image.paste(image.crop((0, 0, image.width, image.height - 47)), (0, 0))
            new_image.paste(bottom_rows, (0, new_image.height - image.height + box_position_y))
            image = new_image

        export_path = dest_path / f"{name}.pdf"
        export_path.parent.mkdir(parents=True, exist_ok=True)
        image.save(dest_path / f"{name}.pdf", "PDF", quality=100, subsampling=0)
