import cv2
import json
import argparse
import csv
import re

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument('-a','--annotations', default="project/output/yolo.txt",type=str,nargs='+', help='Annotation files')    
args = ap.parse_args()

#with open('classes.txt', mode='r') as infile: 
#	mydict =json.load(infile)

with open('classes.csv', mode='r') as infile:
	reader = csv.reader(infile)
	mydict = {str(int(rows[0])):rows[1:] for rows in reader}

#print(mydict)

font                   = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10,100)
fontScale              = 0.5
fontColor              = (255,255,255)
thickness              = 1
lineType               = 2
topLeftCornerOfText    = (10,700)
 
i=0
print(args.annotations)
with open(args.annotations[0], 'r') as f:
	for line in f:
		i=i+1
		if i % 50 == 0:
		#if i  == 100:
			x = re.split(",",line)
			bbox = [float(x[3]),float(x[4]),float(x[5]),float(x[6])]
			fil = x[0]
			fil_native = x[1]
			print(x[2],mydict[x[2]])
			windowname = x[2] + ' '+ mydict[x[2]][0] 
			print(fil)
			image = cv2.imread(fil)
			width=2048
			height=1536
			#Native is centreX, centreY, width, height
			x_min=int((bbox[0]-bbox[2]/2)*width)
			x_max=int((bbox[0]+bbox[2]/2)*width)
			y_min=int((bbox[1]-bbox[3]/2)*height)
			y_max=int((bbox[1]+bbox[3]/2)*height)

			cv2.rectangle(image,(x_min,y_min),(x_max,y_max),(0,255,0),2)
			image = cv2.resize(image, (1024, 768))
			
			cv2.putText(image,fil, 
			    (10,720), 
			    font, 
			    0.3,fontColor,
			    thickness,
                            lineType)
			#print(windowname)
			cv2.putText(image,fil_native,(10,700),font, 
			    fontScale,fontColor,thickness,lineType)
			
			cv2.putText(image,windowname,(10,50),font, 
			    0.7,fontColor,thickness,lineType)

			#cv2.imshow(windowname,image)
			#cv2.waitKey(100)
			#cv2.destroyAllWindows()
			cv2.imwrite("imagebox_"+str(i)+".png",image)
			i=i+1
	    

 
