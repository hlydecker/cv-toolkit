import cv2
import json
import argparse
import csv
import re

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument('-a','--annotations', default="project/output/yolo.txt",type=str,nargs='+', help='Annotation files')    
args = ap.parse_args()
  

with open('classes.txt', mode='r') as infile:
	reader = csv.reader(infile)
	mydict = {str(int(rows[0])-1):rows[1:] for rows in reader}

print(mydict)

font                   = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10,500)
fontScale              = 1
fontColor              = (255,255,255)
thickness              = 1
lineType               = 2
 
i=0
print(args.annotations)
with open(args.annotations[0], 'r') as f:
	for line in f:
		i=i+1
		if i % 100 == 0:
			x = re.split('(.JPG )|(.jpg )',line)
			#print(x)
			x=[a for a in x if a is not None]
			print(x)
			y = x[2].rstrip().split(",")
			bbox=[int(y[0]),int(y[1]),int(y[2]),int(y[3])]
			#print(y)
			fil=x[0]+x[1][:-1]
			#print(fil)
			image = cv2.imread(fil)

			width=2048
			height=1536
			x_min=int(bbox[0])
			y_max=int(bbox[3])
			x_max=int(bbox[2])
			y_min=int(bbox[1])

			cv2.rectangle(image,(x_min,y_min),(x_max,y_max),(0,255,0),2)
			windowname=mydict[y[-1]][0]
			image = cv2.resize(image, (1024, 768))

			cv2.putText(image,windowname, 
			    bottomLeftCornerOfText, 
			    font, 
			    fontScale,
			    fontColor,
			    thickness,
			    lineType)

			#cv2.imshow(windowname,image)
			#cv2.waitKey(100)
			#cv2.destroyAllWindows()
			cv2.imwrite("imagebox_"+str(i)+".png",image)
			i=i+1
	    

 
