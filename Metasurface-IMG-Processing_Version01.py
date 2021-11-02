# -*- coding: utf-8 -*-
"""
Created on Sun Oct 24 19:14:56 2021

@author: frfty
"""

import cv2
import numpy as np 
import matplotlib.pyplot as plt

# =============================================================================
# FOR THE USER TO TYPE IN
# =============================================================================
scaling = 1000 # make this a relatively big number. even if you need to change units 
unit = 'nanometer'
threshold=250
img_name = 'sample03tif.tif'
num_sizes = 10
# to filter out noise in the circle
# if a structure is less than this size in pixel area, it is not a circle 
noiseThreshold = 500 

# =============================================================================
# Read the original image
# =============================================================================
img = cv2.imread(img_name)
imgcopy = img.copy()

# =============================================================================
# scaling
# =============================================================================

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
while img[y,x,0]==0: #go to the right edge of first white tick from left
    x-=1
first_tick = x

while img[y,x,0]!=0: #get past the white stripe 
    x-=1
while img[y,x,0]==0: #get to the right edge of 2nd white tick from left
    x-=1
second_tick = x

# Calculation of units per pixel 
perpixel = scaling/(10*(first_tick - second_tick))
print(perpixel, unit, 'per pixel')

# =============================================================================
# Cropping the image + edge detection 
# =============================================================================

# Cropping the image to remove the bottom stripe 
img_crop = img[0:height]

# Blur the image for better edge detection
img_blur = cv2.GaussianBlur(img_crop, (3,3), 100)

# Canny Edge Detection
edges = cv2.Canny(img_blur, threshold, threshold) 

# Display Canny Edge Detection Image
cv2.imshow('Canny Edge Detection', edges)

# =============================================================================
# Recursive methods to complete a circle 
# =============================================================================

def completeCircle(y,x,bound): 
    y_list = []
    x_list = []
    edges[y,x]=150
    y_list.append(y)
    x_list.append(x)
    
    for j in range(max(0, y-bound), min(height, y+bound)):
        for i in range(max(0,x-bound), min(width, x+bound)):
            if (edges[j,i]==255):
                nextCircle = completeCircle(j,i,bound)
                y_list.extend(nextCircle[0])
                x_list.extend(nextCircle[1])
    return [y_list, x_list]

# =============================================================================
# Finding data for each circle 
# =============================================================================
def findData(circle):
    totalArea = 0
    totalY = 0
    totalX = 0
    y_edges = range(circle[0][0], circle[0][-1])
    temp_radius = (circle[0][-1]-circle[0][0])/2
    temp_ycenter = (circle[0][-1]+circle[0][0])/2
    temp_xcenter = circle[1][0]
    x_leftedges = []
    x_rightedges = []
    
    if temp_xcenter-temp_radius<-30 or temp_xcenter+temp_radius>width+30 or temp_ycenter-temp_radius<-30 or temp_ycenter+temp_radius>height+30:
            return [0,0,0]
    
    for j in y_edges: 
        expect_theta = np.arcsin(abs(j-temp_ycenter)/temp_radius)
        expect_left = int(temp_xcenter - temp_radius*np.cos(expect_theta))
        expect_right = int(temp_xcenter + temp_radius*np.cos(expect_theta))
        if expect_left < -30 or expect_right > width+30: 
            return [0,0,0]
        l_adjusted = False
        r_adjusted = False 
        if j in circle[0]:
            first = min(min(np.where(circle[0]==j)))
            last = max(max(np.where(circle[0]==j)))
            left = min(circle[1][first:last+1])
            right = max(circle[1][first:last+1])
            if abs(left - expect_left)<30 or (x_leftedges and abs(x_leftedges[-1] - left)<30): 
                x_leftedges.append(left)
                l_adjusted = True
            if abs(right - expect_right)<30 or (x_rightedges and abs(x_rightedges[-1] - right)<30):  
                x_rightedges.append(right)
                r_adjusted = True
        if not l_adjusted: 
            if (x_leftedges):
                x_leftedges.append(x_leftedges[-1])
            else:
                x_leftedges.append(expect_left)
        if not r_adjusted: 
            if (x_rightedges):
                x_rightedges.append(x_rightedges[-1])
            else:
                x_rightedges.append(expect_right)
        temp_xcenter = (x_leftedges[-1]+x_rightedges[-1])/2
        for i in range(x_leftedges[-1], x_rightedges[-1]):
            totalY += j
            totalX += i
            totalArea+=1
    if totalArea==0:
        return [0,0,0]
    # 0 Area in pixels, 1 Center y, 2 center x, 
    # 3 y edges, 4 x left edges, 5 x right edges, 
    # 6 area in units, 
    # 7 radius in pixels
    return [int(totalArea), int(totalY/totalArea), int(totalX/totalArea),
            y_edges, x_leftedges, x_rightedges, 
            totalArea*perpixel**2, 
            int(np.sqrt(totalArea/np.pi))]

def roundness(centerX, centerY, x_listL, x_listR, y_list, avgrad): 
    distlist = []
    for k in range(len(y_list)):
        d = np.sqrt((x_listL[k]-centerX)**2+(y_list[k]-centerY)**2)
        distlist.append(d)
        d = np.sqrt((x_listR[k]-centerX)**2+(y_list[k]-centerY)**2)
        distlist.append(d)
    return (max(distlist)-min(distlist))/avgrad
# =============================================================================
# processing each circle 
# =============================================================================

ccthresh = 5

radiuslist = []
arealist = []
datalist = []
for j in range(height):
    for i in range(width):
        if (edges[j][i]==255):
            # get all the raw points that make up the circle edge
            nextcircle = completeCircle(j, i, ccthresh)
            circle = np.array(nextcircle)
            # sort the circle by y-value 
            circle = circle[:, circle[0].argsort()]
            data = findData(circle)
            if data[0]<noiseThreshold: # some "circles" may actually be just noise
                continue
            img[nextcircle] = (0,0,255) # outlining "circles" with red 
            radiuslist.append(data[7])
            arealist.append(data[0])
            datalist.append(data)

# setting color to distinguish areas 

num_sizes=min(num_sizes, len(arealist))
arealist = np.sort(arealist)
prev = arealist[0]
arealist = arealist[1:]
diff_data = [[] for i in range(2)] #where 1st is the area and 2nd is how much bigger is this area than previous
for a in arealist: 
    diff_data[0].append(a)
    diff_data[1].append(a-prev)
    prev = a
# print (diff_data, 'areas and differences')
diff_data1 = np.array(diff_data)
diff_data2 = diff_data1[:, diff_data1[1,:].argsort()]
# print (diff_data, 'sorted by difference')
diff_data3 = diff_data2[:, -num_sizes+1:]
# print (diff_data, 'top',str(num_sizes),'differences and threshold')
diff_data4 = np.sort(diff_data3[0])
print (diff_data1)
    

# =============================================================================
# placing all the info on the original image 
# =============================================================================

# helper method for finding which category an area belongs to 
def findCategory(my_area):
    if len(diff_data4)<1:
        return 0
    for k in range(len(diff_data4)):
        if my_area<diff_data4[k]:
            return k
    return k+1

# actually placing info 

colorlist = np.random.randint(200, size = (num_sizes,3))
size_frequencies = [0]*(num_sizes)
for d in datalist:
    cat = findCategory(d[0])
    size_frequencies[cat]+=1
    color = (colorlist[cat])
    for j in range(len(d[3])):
        for x in range(d[4][j],d[5][j]): 
            # colorscale image colors 
            imgcopy[d[3][j]][x] = color
            
        # now draw the area and rectangle on the image 
        font = cv2.FONT_HERSHEY_SIMPLEX # font 
        fontScale = 0.5  # fontScale
        blue = (255, 0, 0) # Blue color in BGR
        thickness = 1 # Line thickness of 2 px
        
        # drawing the center of rectangle on data image 
        cv2.rectangle(img, (d[2]-5,d[1]-5), (d[2]+5,d[1]+5), (0, 128, 255), -1)
        
        # drawing the area on the area colorscale image
        cv2.putText(imgcopy, "{:.2f}".format(d[6]), (d[2], d[1]), font, fontScale, (255,255,255), thickness, cv2.LINE_AA)
        
        # drawing the diameter data 
        loc = (int(d[2]-d[7]*2/3), int(d[1]-d[7]/4))
        rad = "{:.2f}".format(2*d[7]*perpixel)
        cv2.putText(img, rad, loc, font, fontScale, blue, thickness, cv2.LINE_AA)
        cv2.line(img, (d[2]-d[7], d[1]), (d[2]+d[7], d[1]), blue, 2)
            
        # # drawing the standard deviation data 
        loc = (int(d[2]-d[7]*2/3), int(d[1]+d[7]*1/2))
        rnd = "{:.2f}".format(roundness(d[2], d[1], d[4], d[5], d[3], d[7]))
        cv2.putText(img, 'r='+rnd, loc, font, fontScale, blue, thickness, cv2.LINE_AA)

# data analysis 

if num_sizes>0:
    area_bins = diff_data4.tolist()
    area_bins.insert(0,arealist[0])
    colorlist = [c/255 for c in colorlist]
    order = [2,1,0]
    for i in range(len(colorlist)):
        colorlist[i] = [colorlist[i][j] for j in order]
    x_axis = range(1,num_sizes+1)
    plt.title('Distribution of areas')
    bars=plt.bar(area_bins, size_frequencies, width=1.0, facecolor='black', edgecolor='pink')
    for x,y in zip(x_axis,size_frequencies):
        label = "{:.0f}".format(y)
        plt.annotate(label, (area_bins[x-1],y), textcoords="offset points", xytext=(0,10), ha='center')
        bars[x-1].set_color(colorlist[x-1])


cv2.imshow('Colorscale depending on Area in '+unit+'^2', imgcopy)
cv2.imshow('Average diameter in '+unit+' and roundness where 0 is perfect round', img)