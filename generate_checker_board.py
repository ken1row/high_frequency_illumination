#!/usr/bin/env python
'''
 generate_checker_board.py

 Copyright(c) Photometry group in Yagi lab., ISIR, Osaka University.
     Sep. 2013, Kenichiro Tanaka
     modified: Jan. 2016, Kenichiro Tanaka

 Generate checkerboard for high frequency illumination
'''

import numpy as np
import cv2
#import Image # PIL can be used if you don't want to use Open CV.
import argparse
import sys

def generate(h=768, w=1024, sqsize=9, color1=(0,0,0), color2=(255,255,255), offset_x=0, offset_y=0):
    '''
    Generate checkerboard image.
    
    Parameters
    ----------
    h : int, optional
        Image height.
    w : int, optional
        Image width.
    sqsize : int, optional
        Size of white and black squares.
    color1 : (int, int, int), optional
        Color of the 'black' square.
    color2 : (int, int, int), optional
        Color of the 'white' square.
    offset_x : int, optional
        Checkerboard offset for horizontal axis.
    offset_y : int, optional
        Checkerboard offset for vertical axis.
        
    Returns
    -------
    img : int(h, w, 3)
        Checkerboard image.
    '''
    img = np.zeros((h,w,3), dtype=np.uint8)
    c = np.fromfunction(lambda x,y: (((x+offset_x)//sqsize) + ((y+offset_y)//sqsize)) % 2, (h,w))
    img[c==0]=color1
    img[c==1]=color2
    return img
	
if __name__ == '__main__':
    # Parse program arguments
    parser = argparse.ArgumentParser(description='Generate checkerboard patterns')
    parser.add_argument('-s', '--size', type=int, nargs=2, default=(1024, 768), help="Image size.", metavar=("Width", "Height"))
    parser.add_argument('-q', '--sqsize', type=int, default=9, help="Square size of the pattern.")
    parser.add_argument('-f', '--shift', type=int, default=3, help="Shift amount.")
    parser.add_argument('-o', '--once', action='store_true', default=False, help="Generate only single pattern.")
    parser.add_argument('--color1', type=int, nargs=3, default=(0, 0, 0), help = "Background color.", metavar=("R","G","B"))
    parser.add_argument('--color2', type=int, nargs=3, default=(255, 255, 255), help = "Foreground color.", metavar=("R","G","B"))
    args = parser.parse_args()
    (w, h) = args.size
    sqsize = args.sqsize
    step = args.shift
    color1 = args.color1
    color2 = args.color2

    x = 0
    y = 0
    fnum = 0
    if args.once:
        img = generate(h, w, sqsize, color1, color2, 0, 0)
#        pilImg = Image.fromarray(img, 'RGB')
#        pilImg.save(str(fnum)+'.png')
        cv2.imwrite(str(fnum)+'.png', cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        sys.exit(0)
        
    #
    # white and black
    #
    img = np.zeros((h,w,3), dtype=np.uint8)
    c = np.zeros((h, w))
#    img[c==0]=color1
#    Image.fromarray(img, 'RGB').save('black.png')
    cv2.imwrite('black.png', cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    c = np.ones((h, w)) * 255
#    img[c==1]=color2
#    Image.fromarray(img, 'RGB').save('white.png')
    cv2.imwrite('white.png', cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    
    #
    # Shifting
    #
    while x < sqsize*2:
        y = 0
        while y < sqsize:
            img = generate(h, w, sqsize, color1, color2, x, y)
#            pilImg = Image.fromarray(img, 'RGB')
#            pilImg.save(str(fnum)+'.png')
            cv2.imwrite(str(fnum)+'.png', cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            fnum += 1
            y += step
        x += step
         

