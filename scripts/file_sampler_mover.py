# file_sampler_mover.py
# Utility script to randomly sample and move files from one folder to another

import splitfolders 
import pathlib
import os
import argparse
import pandas as pd
import random
import tqdm


if __name__ == "__main__":

    time_start = pd.Timestamp('now')
    # Define arguments using argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('-i','--images_dir', default="project/images/testing_subset",type=pathlib.Path, help='Input directory')
    ap.add_argument('-o','--output_dir', default="project/images/testing_subset_split",type=pathlib.Path, help='Output directory')
    ap.add_argument('-t','--training_size', default=0.8, type=float, help='The percentage of the dataset to be used for training')
    args = ap.parse_args()

    image_path = args.images_dir

    splitfolders.ratio(image_path, args.output_dir,ratio=(args.training_size, (1-args.training_size)))
