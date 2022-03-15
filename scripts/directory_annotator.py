# directory_annotator.py
# A script that:
# 1. recursively reads through directories, finding all images 
# 2. Extracts EXIF data from images
# 3. Identifies the first species in the image's EXIF keywords
# 4. Writes the image to a new dir with the species name.
# This is silly but YOLO ¯\_(ツ)_/¯

# Imports and constants
import distutils
import shutil
import os
import re
import logging
import pathlib
import pandas as pd
from distutils import file_util
import argparse
import subprocess
from tqdm import tqdm
from itertools import chain
from multiprocessing import Pool
import multiprocessing

if __name__ == "__main__":

    time_start = pd.Timestamp('now')
    # Define arguments using argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('-i','--images_dir', default="project/images/testing_subset",type=pathlib.Path, help='Input directory')
    args = ap.parse_args()

    image_path = args.images_dir

    # TODO: make this a function
    # TODO: make this use multiprocessing
    for file in tqdm(image_path.glob('**/*.JPG')):
        cmd="exiftool -Keywords " + '''"''' + str(file) + '''"'''
        image_keywords = subprocess.getoutput([cmd])
        extracted_keywords = re.findall(r'(?<=a\).)(.*)(?=.\()', image_keywords)
        # check if the image is annotated
        if len(extracted_keywords) == 0:
            # if it isn't, note this
            extracted_keywords.insert(0, "no_annotation")
        
        destination_dir = os.path.join(image_path, str(extracted_keywords[0]).replace(" ","_"))
        # check if the destination directory exists, make it if it doesn't
        if not os.path.exists(destination_dir):
            os.mkdir(destination_dir)
        # move the image to the destination directory
        distutils.file_util.copy_file(file, destination_dir, update=1)
