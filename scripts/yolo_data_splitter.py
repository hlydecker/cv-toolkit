# yolo_data_splitter.py
"""
Split images into training, validation, and test sets.

    Args:
        annotation_file (str): .txt file with info on the images and their annotations.
        image_dir (str): The location where the images are stored.
        training_size (float): The percentage of the dataset to be used for training.
        seed (int): The seed for the random number generator.
    
    Usage:
        python yolo_data_splitter.py --annotation_file=yolo.txt --image_dir=dataset --training_size=0.8

"""
import random
from sklearn.model_selection import train_test_split 
import pathlib
from pathlib import Path
import os
import argparse
import pandas as pd
import random
import csv
import tqdm
import shutil

def yolo_data_group_generator(data_group_df, data_group, bulk_dir):
    """
    Make a folder for the data group if it doesn't exist.
    Copy images into the data group's "images" folder.
    Create annotation files the data group's "labels" folder.

    Args:
        data_group_df (pandas.DataFrame): A dataframe containing the data group's images and labels.
        data_group (str): The name of the data group.
    Usage:
        yolo_data_group_mover(train_df, "train")
    """
    dir_root = os.getcwd()
    if not os.path.isdir(os.path.join(dir_root,data_group)):
        os.mkdir(os.path.join(dir_root,data_group))

    old_path = bulk_dir
    image_dir = os.path.join(data_group,'images')
    if not os.path.isdir(os.path.join(dir_root,image_dir)):
        os.mkdir(os.path.join(dir_root,image_dir))

    for image in data_group_df['filename'].tolist():
        old_file = os.path.join(old_path,image)
        if Path(old_file).exists():
            shutil.copy(old_file, image_dir)
        else:
            print(f"{image} was not found in {old_path}")
    
    labels_dir = os.path.join(data_group, 'labels')
    if not os.path.isdir(os.path.join(dir_root,labels_dir)):
        os.mkdir(os.path.join(dir_root,labels_dir))

    for i, row in data_group_df.iterrows():
        with open(os.path.join(labels_dir, row['filename'].split('.')[0] + '.txt'), 'w') as f:
            f.write(row['classid']+" "+row['x_center']+" "+row['y_center']+" "+row['width']+" "+row['height'])

if __name__ == "__main__":

    time_start = pd.Timestamp('now')
    # Define arguments using argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('-a','--annotation_file', default="yolo.txt",type=str, help='Input .txt file with annotations')
    ap.add_argument('-i','--image_dir', default="project/images/testing_subset",type=pathlib.Path, help='Directory where images are stored')
    ap.add_argument('-t','--training_size', default=0.8, type=float, help='The percentage of the dataset to be used for training')
    ap.add_argument('-s','--seed', default=42, type=int, help='The seed for the random number generator')
    args = ap.parse_args()

    # Read in the bulk annotation .txt file
    annotations_input = args.annotation_file

    with open(annotations_input, 'r') as f:
        annotations = csv.reader(f)
        ann_list = []
        for row in annotations:
            ann_list.append(row)
    
    # Make it a nice dataframe
    annotation_df = pd.DataFrame(ann_list)
    annotation_df.columns = ['filepath','filename','classid','x_center','y_center','width','height']
    annotation_df['classid'] = annotation_df['classid'].astype('str')

    # Test/Val/Train splitting
    random.seed(args.seed)
    test_val_size = 1 - args.training_size

    train, test_val = train_test_split(annotation_df, test_size = test_val_size, stratify = annotation_df['classid'])

    val, test = train_test_split(test_val, test_size = 0.5, stratify = test_val['classid'])

    # Make the data groups
    yolo_data_group_generator(train, data_group='train',bulk_dir=args.image_dir)
    yolo_data_group_generator(val, data_group='val',bulk_dir=args.image_dir)
    yolo_data_group_generator(test, data_group='test',bulk_dir=args.image_dir)