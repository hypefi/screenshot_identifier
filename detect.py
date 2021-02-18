import cv2
import pytesseract
import numpy as np
import sys
import getopt
import os
from urllib.parse import urlparse


print ("Number of arguments:", len(sys.argv), "arguments.")

print ("Argument List:", str(sys.argv))


url = "." + sys.argv[1]
print(url)

img = cv2.imread(url)                       #Alternatively: can be skipped if you have a Blackwhite image
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
gray, img_bin = cv2.threshold(gray,128,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
gray = cv2.bitwise_not(img_bin)


kernel = np.ones((2, 1), np.uint8)
img = cv2.erode(gray, kernel, iterations=1)
img = cv2.dilate(img, kernel, iterations=1)
out_below = pytesseract.image_to_string(img)
print("OUTPUT:", out_below)

#change file name from title

path = os.path.dirname(url)
print(path)
newfilename = path + "/" + out_below
print(newfilename)
os.rename(url,newfilename)


