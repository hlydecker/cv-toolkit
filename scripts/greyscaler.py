# greyscaler.py
# Broken and bad script that fails at turning images from rgb to greyscale
# TODO: FIXME :D
# NOTE: Is there any utility to this vs imagemagick? Maybe for windows use?
from skimage import io, color
import pathlib
import os
import re
import distutils
import shutil
import os
import glob
import re
import logging
import pathlib
import pandas as pd
from distutils import file_util
import argparse
from tqdm import tqdm
from itertools import chain
from multiprocessing import Pool
import multiprocessing
import imghdr
import tqdm
import argparse

if __name__ == "__main__":

    time_start = pd.Timestamp('now')
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('-i','--images_dir', default="project/images/rgb",type=pathlib.Path, help='Input directory')
    ap.add_argument('-o','--output_dir', default="project/images/bw",type=pathlib.Path, help='Output directory')
    args = ap.parse_args()

    image_path = args.images_dir
    destination_dir = args.output_dir

    # check if the destination directory exists, make it if it doesn't
    if not os.path.exists(destination_dir):
        os.mkdir(destination_dir)

    for file in tqdm(image_path.glob('**/*.JPG')):
        rgb = io.imread(file)
        grey = color.rgb2gray(rgb)
        head, tail = os.path.split(file)
        io.imsave(os.path.join(destination_dir, tail), grey)
        