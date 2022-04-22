# yolo_hardcoded_recoder.py
'''
This is a dumb script that fixes an even dumber problem.

Let's say we've gone to the pain of collecting a bunch of images, and getting people to annotate them.
What if these people entered their annotations in MANUALLY using hand typing, rather than selecting from a dropdown?
Of course we will encounter mistakes.

This script will:
1. Recursively read in YOLO format .txt annotations
2. Recode the classes is they are one of the broken ones
3. Save the fixed annotations in a new dir. It is up to you to then decide what to do with the broken ones.
'''

# Imports and constants
from cgitb import text
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

def recode_classes(class_id):
    """
    This function will fix the broken classes.

    Don't judge me for this please :(
    
    :param class_id: The class id to recode
    :return: class_id: The recoded class id
    """
    # TODO: Make this take a dict of classes to recode, instead of just hardcoding it. 
    # At the moment I am too lazy to actually code out a function to generate an adaptive if else statement.

    # This is very sad but here we go...
    if class_id == "10":
        class_id = "8"
    elif class_id == "11":
        class_id = "10"
    elif class_id == "12":
        class_id = "11"
    elif class_id == "13":
        class_id = "12"
    elif class_id == "14":
        class_id = "13"
    elif class_id == "15":
        class_id = "3"
    elif class_id == "16":
        class_id = "14"
    elif class_id == "17":
        class_id = "15"
    elif class_id == "18":
        class_id = "16"
    elif class_id == "19":
        class_id = "17"
    elif class_id == "20":
        class_id = "18"
    elif class_id == "21":
        class_id = "19"
    elif class_id == "22":
        class_id = "20"
    elif class_id == "23":
        class_id = "21"
    elif class_id == "24":
        class_id = "22"
    elif class_id == "25":
        class_id = "23"
    elif class_id == "26":
        class_id = "24"
    elif class_id == "27":
        class_id = "25"
    elif class_id == "28":
        class_id = "26"
    elif class_id == "29":
        class_id = "27"
    elif class_id == "30":
        class_id = "28"
    elif class_id == "31":
        class_id = "29"
    elif class_id == "32":
        class_id = "30"
    elif class_id == "33":
        class_id = "31"
    elif class_id == "34":
        class_id = "18"
    elif class_id == "35":
        class_id = "4"
    elif class_id == "36":
        class_id = "32"
    elif class_id == "37":
        class_id = "33"
    elif class_id == "38":
        class_id = "15"
    elif class_id == "39":
        class_id = "34"
    elif class_id == "40":
        class_id = "28"
    elif class_id == "41":
        class_id = "35"
    elif class_id == "42":
        class_id = "36"

    return class_id

def fix_yolo_classes(yolo_string):

    yolo_string = yolo_string.split(" ")
    yolo_string_list = [str(x) for x in yolo_string]
    yolo_string_list[0] = recode_classes(yolo_string_list[0])
    yolo_string_fixed = " ".join(yolo_string_list)

    return(yolo_string_fixed)

if __name__ == "__main__":

    time_start = pd.Timestamp('now')
    # Define arguments using argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('-a','--annotation_dir', default="project/images/testing_subset",type=pathlib.Path, help='Input directory')
    args = ap.parse_args()

    ann_path = args.annotation_dir

    for text_file in tqdm(ann_path.glob("*.txt")):

        with open(text_file, 'r') as f:
            yolo_string = f.read()

        yolo_string_fixed = fix_yolo_classes(yolo_string)


        destination_dir = os.path.join(ann_path, "fixed")
        # check if the destination directory exists, make it if it doesn't
        # if not os.path.exists(destination_dir):
        #     os.mkdir(destination_dir)
        
        with open(text_file, 'w') as f:
            f.write(yolo_string_fixed)



