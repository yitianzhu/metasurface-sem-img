# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 12:27:19 2021

@author: frfty
"""
# For the user to fill out 
img_filename = 'sample03tif.tif' 
threshold=100

import cv2
import numpy as np
# Read the original image
img = cv2.imread(img_filename)

# Getting the height and width of the image 
height = img.shape[0]
width = img.shape[1]

# reading the image tick marks to get scaling factor 
y = height-1 # self note - coordinates in y, x, c. 
x = width-1
while img[y,x,0]==0: #get up to the y level of white ticks 
    y-=1
y+=1
height=y

# Cropping the image to remove the bottom stripe 
img_crop = img[0:height]

# Blur the image for better edge detection
img_blur = cv2.GaussianBlur(img_crop, (3,3), 100)

# Canny Edge Detection
edges = cv2.Canny(img_blur, threshold, threshold) 

# Display Canny Edge Detection Image
cv2.imshow(img_filename+' ('+str(threshold)+','+str(threshold)+')', edges)

print(np.count_nonzero(edges)/(width*height))