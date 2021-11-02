# SEM Image Processing for Metasurfaces
## Version 1.0

This mini-program will take in an SEM image and measure the dimensions of circular metaatoms. 
It uses Canny edge detection, recursion, and loops to process each metaatom feature pixel by pixel. 

## Program Workflow 
1) Given an original image, the program first uses Canny edge detection to find the edges
//INSERT ORIGINAL PLUS CANNY
2) The program then identifies individual metaatoms using the black and white edge image. 
3) For each metaatom, the program will measure area, average diameter, roundness (where a perfect circle is 0), etc. This information will be displayed on an image, as shown below
// INSERT IMAGE OF DIAMETER AND ROUNDNESS DATA
4) The program will classify the metaatoms by size. Each size category will be represented visually by a single color. The number of metaatoms in each size category will be reflected in the bar graph.
// INSERT IMAGE OF BAR GRAPH 

## How to use the program 

### Part 1: Downloads
Download the following into one folder:
* Canny_threshold_finder.py
* Metasurface-Img-Processing_Version01.py 
* All the images you would like to process

### Part 2: Manually finding a threshold 
You will use the Canny_threshold_finder.py program for this part. Open this program in your Python console. <br/>
1) Fill out the following information at the beginning of the program. 
```markdown
# This is the name of your image file 
img_filename = 'sample03tif.tif' 
# This is a starting test value. 
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
# This number should be printed in the black band at the bottom of the SEM image. 
scaling = 1000 
# This unit should be printed in the black band at the bottom of the SEM image
unit = 'nanometer' 
# This number is the same optimal threshold you found in Part 2. 
threshold=110 
# This is the file name 
img_name = 'sample01tif.tif' 
# The program will classify metaatoms by size. This is the number of categories you would like to see. 
num_sizes = 10 
```
2) Run the program. 
