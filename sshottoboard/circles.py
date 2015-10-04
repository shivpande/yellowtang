import cv2
import sys
import numpy as np
import subprocess
import time

import cv2.cv as cv

infile = cv2.imread(sys.argv[1],0)
outfile = time.strftime("%H%M%S")+'circle-'+sys.argv[1]
print outfile

#infile = cv2.cvtColor(infile,cv2.COLOR_GRAY2BGR)
circles = cv2.HoughCircles(infile,cv.CV_HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=10,maxRadius=50)
print "TODO: EDIT MIN/MAX THRESHOLDS"
print "HoughCircles*"
#print type(circles)
#print circles.dtype
#print '*************************circlesndarray'
#print circles
#print '*************************'
circles=circles.tolist()[0]
#print type(circles)
#print len(circles)
print '*************************circlestolist'
print('\n'.join([''.join(['{:4}\t'.format(item) for item in row]) for row in circles]))
print '*************************'

sortedcircles =  sorted(circles,key=lambda x: x[1])
print '*************************sortedcircles'
print('\n'.join([''.join(['{:4}\t'.format(item) for item in row]) for row in sortedcircles]))
print '*************************'
circleradii = sorted([int(x[2]) for x in circles])
counts = np.bincount(np.array(circleradii))
circleradii_mode = np.argmax(counts)
print 'circleradii: '+ str(circleradii)
print 'circleradii_mode: '+ str(circleradii_mode)


print 'get rid of last 5'
last5 = [x[1] for x in sortedcircles[-5:]]
print '*************************last5'
print last5
print '*************************'
if len(set(last5)) != 1 and set(last5[:-4]) != 1 :
	print "last5 aren't equal, aborting"
	exit()
randombottomcircle = sortedcircles[-1]
print str(randombottomcircle)

circles=sortedcircles[:-5]
circles = [circles]
circles = np.asarray(circles)
print type(circles)
print circles.dtype
print '*************************circlesndarray'
print circles
print '*************************'
print "no we can crop the bottom of the image with randombottomcircle*"
height, width = infile.shape[:2]
print 'h: %d\tw: %d' % (height, width)
bottomcircleradius = randombottomcircle[2]
bottomcircleyval = randombottomcircle[1]
bottomcirclecropy = int(float(bottomcircleyval)-float(bottomcircleradius))

print bottomcircleradius
print bottomcircleyval
print bottomcirclecropy
croppedinfile = infile[0:bottomcirclecropy,0:width]





















print 'attaching circles to cropped image'
circles = np.uint16(np.around(circles))
print "uint16*"
for i in circles[0,:]:
	# draw the outer circle
	cv2.circle(croppedinfile,(i[0],i[1]),i[2],(0,255,0),2)
	# draw the center of the circle
	cv2.circle(croppedinfile,(i[0],i[1]),2,(0,0,255),3)


cv2.imwrite(outfile,croppedinfile)
subprocess.call(['open', outfile])


#cv2.imshow('detected circles',cvt)
#cv2.waitKey(0)
#cv2.destroyAllWindows()