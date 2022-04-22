# yolo_dataset_checker.py

# Imports
import argparse
import csv
import fnmatch
import pprint
import os
import torch
from tqdm import tqdm
import pandas as pd
import yaml
import pathlib
from pathlib import Path 
import numpy as np

# Constants
def read_yolo_yaml(yolo_yaml):
    '''
    Reads in a yolo dataset yaml file.
    '''
    with open(yolo_yaml, 'r') as file:
        yolo_dict = yaml.safe_load(file)
    return(yolo_dict)

def make_class_df(yolo_dict):
    """
    Make a dataframe of the classes in the yolo dataset.
    Dataframe has the following columns:
        classid (str): The class id. Class ids start from 0.
        class (str): The class name.

    Note: These must match what is present in your yolo annotations!
    """
    yolo_classes = pd.DataFrame(yolo_dict['names']).rename_axis('classid').reset_index()
    yolo_classes.columns = ['classid','class']
    yolo_classes['classid'] = yolo_classes['classid'].astype('str')
    yolo_classes

    return(yolo_classes)

def read_annotation(ann_file):
    """
    Read in a yolo annotation file.
    These are individual files for each image, stored in labels/<image_name>.txt
    """
    with open(ann_file) as file:

        csv_ann = csv.reader(file,delimiter=' ')
        ann_list = []
        for row in csv_ann:
            ann_list.append(row)
    return(ann_list)
    
def read_annotation_group(ann_dir,ann_group):

    """
    Read in a yolo annotations for each data group.
    There should be three data groups:
        train
        val
        test
    """
    
    annotations = [] 
    
    ann_dir = pathlib.Path(ann_dir)
    
    for ann_file in tqdm(ann_dir.glob("*.txt")):
        
        ann = read_annotation(ann_file)
        ann = pd.DataFrame(ann)
        ann['filename'] = ann_file
        annotations.append(ann)
                       
    annotations_df = pd.concat(annotations)
    annotations_df['data_group'] = ann_group
    annotations_df.columns = ['classid','x_center','y_center','width','height','filename','data_group']
    return(annotations_df)

def read_annotations(yolo_yaml):

    """
    1. Read in a yolo dataset yaml file.
    2. Find and read the annotation files.
    3. Return a dataframe with the annotations.

    Args:
        yolo_yaml (str): The path to the yolo dataset yaml file.
    
    Returns:
        annotations_df (pd.DataFrame): A dataframe with the annotations.
    """

    yolo_dict = read_yolo_yaml(yolo_yaml)
    
    # Generate paths for each data group
    train_ann_dir = os.path.join(yolo_dict['path'],"train","labels")
    val_ann_dir = os.path.join(yolo_dict['path'],"val","labels")
    test_ann_dir = os.path.join(yolo_dict['path'],"test","labels")
    
    # Create dataframes for each data group
    train_anns = read_annotation_group(train_ann_dir, "train")
    val_anns = read_annotation_group(val_ann_dir, "val")
    test_anns = read_annotation_group(test_ann_dir, "test")
    
    # Create a dict of class names
    yolo_classes = make_class_df(yolo_dict)
    
    ann_df = pd.concat([train_anns, val_anns, test_anns], axis=0)
    ann_df = pd.merge(ann_df, yolo_classes, on='classid')
    
    return(ann_df)

def summarise_yolo_dataset(ann_df):

    """
    WIP: Summarise the yolo dataset.
    """
    
    print(ann_df.groupby('data_group',as_index=False)['class'].nunique())
    
    print('Classes in training')
    print(ann_df.loc[ann_df['data_group'] == 'train'].groupby(['class','data_group'],as_index=False).agg({'data_group': 'count'}))
    print('Classes in validation')
    print(ann_df.loc[ann_df['data_group'] == 'val'].groupby(['class','data_group'],as_index=False).agg({'data_group': 'count'}))
    print('Classes in testing')
    print(ann_df.loc[ann_df['data_group'] == 'test'].groupby(['class','data_group'],as_index=False).agg({'data_group': 'count'}))
    train_classes = ann_df.loc[ann_df['data_group'] == 'train'].groupby(['class','data_group'],as_index=False).agg({'data_group': 'count'})
    val_classes = ann_df.loc[ann_df['data_group'] == 'val'].groupby(['class','data_group'],as_index=False).agg({'data_group': 'count'})
    test_classes = ann_df.loc[ann_df['data_group'] == 'test'].groupby(['class','data_group'],as_index=False).agg({'data_group': 'count'})
    
    train_val_diff = np.setdiff1d(train_classes['class'],val_classes['class'])
    train_test_diff = np.setdiff1d(train_classes['class'],test_classes['class'])
    
    if len(train_val_diff) > 0:
        print("Validation set is missing ",len(train_val_diff)," classes that are present in the training set.")
    else:
        print("Validation and training contain the same classes")
    if len(train_test_diff) > 0:
        print("Testing set is missing ",len(train_test_diff)," classes that are present in the training set.")
    else:
        print("Testing and training contain the same classes")

if __name__ == "__main__":

    # Define arguments using argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('-y','--yolo_dataset_yaml',type=str, help='YOLO dataset yaml file.')
    ap.add_Argument('-s','--save_csv',type=bool,default=False, help='Save the dataframe as a csv file.')
    args = ap.parse_args()

    annotations_df = read_annotations(args.yolo_dataset_yaml)

    summarise_yolo_dataset(annotations_df)

    if args.save_csv == True:
        annotations_df.to_csv(os.path.join("annotations.csv"))