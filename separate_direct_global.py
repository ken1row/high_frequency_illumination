#!/usr/bin/python
'''
 HighFreqIll.py
     depending on OpenCV, numpy

 Copyright(c) Photometry G. in Yagi lab., ISIR, Osaka University.
     Sep. 2013, Kenichiro Tanaka



 Separate into direct and global components.

 
 Notes
 -----
 1. All images in the directory are loaded for separation.
 2. Black bias is automatically enabled if there is 'black.png'.
 3. Normal illumination is automatically ignored if there is 'white.png'.
 4. -w option is not worked propery unless the images are 16-bits.
'''

import argparse
import glob
import sys
import numpy as np
import cv2

# Parse program arguments
parser = argparse.ArgumentParser(description='Separate into direct and global components.',
                                 epilog='Note:\n1. All images in the directory are loaded for separation.\n 2. Black bias is automatically enabled if there is \'black.png\'.\n 3. Normal illumination is automatically ignored if there is \'white.png\'\n 4. -w option is not worked propery unless the images are 16-bits.')
parser.add_argument('-v', dest='max_min_output', default=False, action='store_true' , help="outputs max and min images")
parser.add_argument('-e', '--extension', default=".png", help="file extension of all images. default is .png")
parser.add_argument('-d', '--dir', default="./", help="image directory. default is current directory.");
parser.add_argument('-w', '--whiteout', default=False, action='store_true', help = "Processing mode when all images are saturated. If set, direct component becomes white, otherwise becomes black.")
args = parser.parse_args()

# Variables
black_bias = False

# Get input filenames
dir = args.dir
extension = args.extension
if not dir.endswith('/'):
	dir = dir + '/'
if not extension.startswith('.'):
	extension = '.' + extension
search_sequence = dir + "*" + extension
black_file = dir + "black" + extension
white_file = dir + "white" + extension
files = glob.glob(search_sequence)
if black_file in files:
	black_bias = True
	files.remove(black_file)
if white_file in files:
	files.remove(white_file)

# If file does not exist, exit the program
if len(files) == 0:
	print "No images..."
	sys.exit()

# Load images
img = cv2.imread(files[0], -1)
max_img = img
min_img = img
for filename in files:
	img = cv2.imread(filename, -1)
	max_img = np.maximum(max_img, img)
	min_img = np.minimum(min_img, img)

# If all images are satulated, direct image should be white?
if args.whiteout:
   min_img[min_img==65535] = 0

# Separate into direct and global components
if black_bias:
    # subtract black bias with underflow prevention
    black_img = cv2.imread(black_file, -1)
    max_img = np.maximum(max_img - black_img, 0)
    min_img = np.maximum(min_img - black_img, 0)
direct_img = max_img - min_img

# Prevent overflow
intensity_max = 65535.0
if max_img.itemsize == 1:
	intensity_max = 255.0
max_img = intensity_max * np.ones(max_img.shape)
global_img = np.uint16(np.minimum(max_img, 2.0 * min_img))

# Save images
cv2.imwrite(dir + "direct" + extension, direct_img)
cv2.imwrite(dir + "global" + extension, global_img)
if args.max_min_output:
	cv2.imwrite(dir + 'max' + extension, max_img)
	cv2.imwrite(dir + 'min' + extension, min_img)

