import os
from pathlib import Path
import time
import shutil
import cv2
from PIL import Image
from tqdm import tqdm
import rich
from omegaconf import OmegaConf, DictConfig
from typing import Dict, List
from PIL import Image, ImageOps
import photohash

from usls.src.utils import (
    CONSOLE, IMG_FORMAT, VIDEO_FORMAT, LABEL_FORMAT, 
    smart_path, get_md5, verify_images, time_now
)
    


def deduplicate(
        directory, 
        directory_duplicated, 
        directory_deprecated, 
        simple=False,
        similarity=False,
        distance=3,
    ):


    # get files
    f_list = [x for x in Path(directory).iterdir() if x.suffix.lower() in IMG_FORMAT]
    CONSOLE.log(f"Find {len(f_list)} files (image file only: {IMG_FORMAT}).")


    # saveout directory: increment
    directory_duplicated = smart_path(Path(directory_duplicated), exist_ok=False, sep='-')  # duplicated
    directory_duplicated.mkdir(parents=True, exist_ok=True)  # make dir
    directory_deprecated = smart_path(Path(directory_deprecated), exist_ok=False, sep='-')  # deprecated
    directory_deprecated.mkdir(parents=True, exist_ok=True)  # make dir


    # way 1
    if simple:
        with CONSOLE.status("[bold green]Checking integrity & De-duplicating...") as status:

            md5_img_dict = {}   # {md5: img_path}
            for p in f_list:  # loop
                if verify_images(path=p, output_dir=directory_deprecated):
                    md5 = get_md5(str(p))

                    # compare and save 
                    if md5 in md5_img_dict.keys():
                        similar_img_path = md5_img_dict[md5]
                        shutil.move(str(p), str(directory_duplicated))
                    else:
                        md5_img_dict[md5] = p


        # conclude
        f_left_list = [x for x in Path(directory).iterdir() if x.suffix.lower() in IMG_FORMAT]
        f_duplicated_list = [x for x in Path(directory_duplicated).iterdir() if x.suffix.lower() in IMG_FORMAT]
        f_deprecatde_list = [x for x in Path(directory_deprecated).iterdir() if x.suffix.lower() in IMG_FORMAT]



    # way 2
    if similarity:

        # remove deprecated images
        with CONSOLE.status("[bold green]Checking integrity...") as status:
            for p in f_list:
                verify_images(path=p, output_dir=directory_deprecated)

        # De-duplicating almost O(n^2)
        with CONSOLE.status("[bold green]De-duplicating base on similarity (it will cost much time)...") as status:
            f_left_list = [x for x in Path(directory).iterdir() if x.suffix.lower() in IMG_FORMAT]

            f_save = list()
            f_duplicated_list = list()

            # loop
            while len(f_left_list) > 0:
                f_save.append(f_left_list.pop(0))  # pop 1st

                # get similarity list
                is_similar_list = []
                for p in f_left_list:
                    is_similar_list.append(photohash.is_look_alike(f_save[-1], p, tolerance=distance))

                # update
                duplicate_items = [x for x, y in zip(f_left_list, is_similar_list) if y]  # duplicates
                f_duplicated_list.extend(duplicate_items)
                [f_left_list.remove(x) for x in duplicate_items]


            # conclude
            f_left_list = f_save
            f_deprecatde_list = [x for x in Path(directory_deprecated).iterdir() if x.suffix.lower() in IMG_FORMAT]


            # remove duplicated files
            for f in f_duplicated_list:
                shutil.move(str(f), str(directory_duplicated))



    # clean up dirs
    if len(f_duplicated_list) == 0:
        directory_duplicated.rmdir()  # rmdir
    if len(f_deprecatde_list) == 0:
        directory_deprecated.rmdir()  # rmdir

    # log
    if len(f_list) == len(f_left_list):
        CONSOLE.log(f"😃 Nothing changed! All images are perfectly unique and well integrated!")
    else:
        CONSOLE.log(f"Task complete ✅")


    # display
    table = rich.table.Table(
        title='\n', 
        title_style='left',
        box=rich.box.ASCII,   # box.MARKDOWN ,SIMPLE   , rich.box.ASCII2
        show_lines=False, 
        show_header=True,
        caption=f"{time_now()}\n",
        caption_justify='center',
        header_style='',
        show_footer=False,
    )

    table.add_column(header="Type", justify="left", no_wrap=False)
    table.add_column(header="Num", justify="left", no_wrap=False)
    table.add_column(header="Path", justify="left", no_wrap=False)


    table.add_row(f"Original", f"{len(f_list)}", f"{Path(directory).resolve()}", end_section=False)
    table.add_row(f"Left", f"{len(f_left_list)}", f"{Path(directory).resolve()}", end_section=False)
    table.add_row(
        f"Duplicated", 
        f"{len(f_duplicated_list)}", 
        f"{directory_duplicated.resolve() if len(f_duplicated_list) > 0 else '---'}", 
        end_section=False
    )
    table.add_row(
        f"Deprecated", 
        f"{len(f_deprecatde_list)}", 
        f"{directory_deprecated.resolve() if len(f_deprecatde_list) > 0 else '---'}",
        end_section=False
    )
    CONSOLE.print(table)




def run_deduplicate(args: DictConfig):
    # with CONSOLE.status("[bold green]Checking & De-duplicating...") as status:
    deduplicate(
        directory=args.dir, 
        directory_duplicated=args.duplicated_dir, 
        directory_deprecated=args.deprecated_dir, 
        simple=args.simple,
        similarity=args.similarity,
        distance=args.distance,
    )
