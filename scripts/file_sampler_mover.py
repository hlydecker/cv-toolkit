# file_sampler_mover.py
# Utility script to randomly sample and move files from one folder to another

import splitfolders 
import pathlib
import os
import argparse
import pandas as pd
import random
import tqdm

# Another option, from https://colab.research.google.com/github/google-research/vision_transformer/blob/master/vit_jax_augreg.ipynb#scrollTo=JOtCfWFOfVFq
#def split(base_dir, test_ratio=0.1):
#  paths = glob.glob(f'{base_dir}/*/*.jpg')
#  random.shuffle(paths)
#  counts = dict(test=0, train=0)
#  for i, path in enumerate(paths):
#    split = 'test' if i < test_ratio * len(paths) else 'train'
#    *_, class_name, basename = path.split('/')
#    dst = f'{base_dir}/{split}/{class_name}/{basename}'
#    if not os.path.isdir(os.path.dirname(dst)):
#      os.makedirs(os.path.dirname(dst))
#    shutil.move(path, dst)
#    counts[split] += 1
#  print(f'Moved {counts["train"]:,} train and {counts["test"]:,} test images.')


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
