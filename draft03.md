# SEM Image Processing for Metasurfaces
## Version 1.0

This mini-program will take in an SEM image and measure the dimensions of circular metaatoms. 
It uses Canny edge detection, recursion, and loops to process each metaatom feature pixel by pixel. 

## How to use 

### Part 1: Downloads
Download the following into one folder:
* Canny_threshold_finder.py
* Metasurface-Img-Processing_Version01.py 
* All the images you would like to process

/// INSERT SCREENSHOT HERE


### Part 2: Manually finding a threshold 
You will use the Canny_threshold_finder.py program for this part. Open this program in your Python console. <br/>
1) In the first row, type the name of your image file. In the second row, type out a starting number (ideally 100). 
```markdown
# For the user to fill out 
img_filename = 'sample03tif.tif' 
threshold=100
```
2) Run the Canny_threshold_finder.py program. An image with the detected edges (in white) should appear. 
* If the image produces clear circles, the threshold number you chose was optimal. 
/// INSERT SCREENSHOT HERE
* If the image has too much noise, increase the threshold number. 
/// INSERT SCREENSHOT
* If the circles are incomplete, decrease the threshold number. 
/// SCREENSHOT 
3) Continue changing the threshold and re-running the program until the program produces clear circles. 

### Part 3: Using the program 
You will use the _ program for this part. Open this program in your Python console. 
1) In the top portion of the program, fill out the following information 
``` markdown
scaling = 1000 # This number should be printed in the black band at the bottom of the SEM image. 
unit = 'nanometer' # This unit should be printed in the black band at the bottom of the SEM image
threshold=110 #This number is the same optimal threshold you found in Part 2. 
img_name = 'sample01tif.tif' # This is the file name 
num_sizes = 10 # The program will classify metaatoms by size. This is the number of categories you would like to see. 
```
