# cv-toolkit
Various random computer vision utility scripts, mostly Python or shell.

## Current Scripts

### Python
1. directory_annotator.py - move images into directories that have names based on their classes. Useful for classification tasks.
2. file_sampler_mover.py - performs random sampling and moves files to different directories based on the data group they are in (e.g. train, test, val).
3. general_json2yolo.py - broken json to yolo converter.
4. greyscaler.py - turns rgb images to greyscale. Generally I would recommend doing this with [bash](#turn-rgb-into-greyscale) instead if you can.
5. yolo_data_splitter.py - read in a text file of concatenated yolo annotations and then perform stratified random sampling to move images to the appropriate image directory, and create text annotations in the appropriate label directory.
6. yolo_dataset_checker.py - script to explore your data and find out if anything weird is going on.
7. yolo_hardcoded_recoder.py - a dangerous tool that lets you recode your yolo annotation classids if there was a mistake somewhere.

# Useful Bash Utilities

## Turn rgb into greyscale

```bash
# single version
magick mogrify -colorspace gray *.jpg

# parallel version
parallel -X magick mogrify -colorspace gray ::: *.jpg
```

## Find and count all images in a directory

```bash
find . -type f | sed -e 's/.*\.//' | sort | uniq -c | sort -n | grep -Ei '(tiff|bmp|jpeg|jpg|png|gif)$'
```
