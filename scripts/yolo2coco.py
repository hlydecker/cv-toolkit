import json
import os

# Create a dictionary to store the COCO format data
coco_data = {
    "images": [],
    "annotations": [],
    "categories": []
}

# Read the YOLO format data from a text file
with open("yolo.txt", "r") as f:
    yolo_data = [line.strip().split(" ") for line in f.readlines()]

# Create a set to store the unique image filenames
filenames = set()

# Create a set to store the unique class labels
class_labels = set()

# Iterate through the YOLO format data
for data in yolo_data:
    # Get the class label, center point, and bounding box dimensions
    class_label = int(data[0])
    xcenter = float(data[1])
    ycenter = float(data[2])
    bbox_width = float(data[3])
    bbox_height = float(data[4])
    image_filename = data[5]
    width, height = int(data[6]), int(data[7])
    
    # Add the image filename and class label to the sets
    filenames.add(image_filename)
    class_labels.add(class_label)
    
    # Calculate the bounding box coordinates
    xmin = xcenter - bbox_width / 2
    ymin = ycenter - bbox_height / 2
    xmax = xcenter + bbox_width / 2
    ymax = ycenter + bbox_height / 2
    
    # Add the annotation to the COCO format data
    coco_data["annotations"].append({
        "image_id": image_filename,
        "category_id": class_label,
        "bbox": [xmin, ymin, xmax, ymax],
        "iscrowd": 0
    })

# Create a list of categories in the COCO format
categories = [{"id": i, "name": str(i)} for i in class_labels]
coco_data["categories"] = categories

# Create a list of images in the COCO format
images = [{"id": f, "file_name": f, "width": width, "height": height} for f in filenames]
coco_data["images"] = images

# Save the COCO format data to a json file
with open("coco.json", "w") as f:
    json.dump(coco_data, f)
