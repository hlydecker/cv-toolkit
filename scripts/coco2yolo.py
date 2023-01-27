import json
import os

# Load the COCO json file
with open("coco.json", "r") as f:
    coco = json.load(f)

# Create a list to store the YOLO format data
yolo_data = []

# Iterate through all images in the COCO dataset
for image in coco["images"]:
    # Get the image filename and size
    filename = image["file_name"]
    width = image["width"]
    height = image["height"]
    
    # Iterate through all annotations for the image
    for annotation in image["annotations"]:
        # Get the class label and coordinates of the bounding box
        class_label = annotation["category_id"]
        xmin, ymin, width, height = annotation["bbox"]
        xmax = xmin + width
        ymax = ymin + height
        
        # Calculate the center point and width and height of the bounding box
        xcenter = (xmin + xmax) / 2
        ycenter = (ymin + ymax) / 2
        bbox_width = xmax - xmin
        bbox_height = ymax - ymin
        
        # Normalize the coordinates to the size of the image
        xcenter /= width
        ycenter /= height
        bbox_width /= width
        bbox_height /= height
        
        # Add the data to the YOLO format list
        yolo_data.append([class_label, xcenter, ycenter, bbox_width, bbox_height])

# Save the YOLO format data to a text file
with open("yolo.txt", "w") as f:
    for data in yolo_data:
        f.write(" ".join([str(x) for x in data]) + "\n")
