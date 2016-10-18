# import the necessary packages
from imutils.video import WebcamVideoStream
import imutils
import cv2
import numpy as np
from networktables import NetworkTable

# Change to 'True' to enable visual output
isDebug = True

# Set up NetworkTables
NetworkTable.setIPAddress("172.16.254.8")
NetworkTable.setClientMode()
NetworkTable.initialize()
vp = NetworkTable.getTable("Vision")

# Init webcam
vs = WebcamVideoStream(src=0).start()

while True: # Loops
    # Grab frame from webcam
    frame = vs.read()
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Blur image to reduce noise
    img = cv2.GaussianBlur(hsv,(7,7), 0)
    
    # frameDelta = cv2.absdiff(baseFrame, img) # Do I want this?

    
    # Define range of green color in HSV
    lower_green = np.array([60,175,140]) # Find these values with GRIP
    upper_green = np.array([180,255,255]) # Find these values with GRIP

    # Threshold the HSV image to get only green colors
    mask = cv2.inRange(img, lower_green, upper_green)
    
    # Erode to remove noise, then dilate to restore size
    kernel = np.ones((5,5),np.uint8)
    mask = cv2.erode(mask,kernel,iterations = 1)
    msak = cv2.dilate(mask,kernel,iterations = 1)
	
    # Bitwise-AND mask and original image (This is optional for targeting)
    if isDebug:
        res = cv2.bitwise_and(img,frame, mask= mask) 

    # Find our contour, get the convex hull, and put that in 'box'
    im2, contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    # Only run if we have a contour (Without this, it just crashes w/o a contour)
    if len(contours) > 0:
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 500:
                cnt = contours[0]
                hull = cv2.convexHull(cnt)
                rect = cv2.minAreaRect(hull)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                
                # Draw contour on debug output
                if isDebug: 
                    cv2.drawContours(res, [box], -1, (255,0,128), 2)
                        
                # Send data to NetworkTables
                M = cv2.moments(box)
                if M["m00"] != 0:
                    centerX = int(M["m10"] / M["m00"])
                    centerY = int(M["m01"] / M["m00"])
                else:
                    centerX, centerY = 0, 0
                area = cv2.contourArea(box)
                perimeter = cv2.arcLength(box,True)
                vp.putNumber('centerX', centerX)
                vp.putNumber('centerY', centerY)
                vp.putNumber('area', area)

    # Show debug output
    if isDebug:
        cv2.imshow('Result', res)
    cv2.waitKey(5)

# Close debug output on exit
if isDebug:
	cv2.destroyAllWindows()
vs.stop()
