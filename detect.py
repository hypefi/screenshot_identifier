import cv2
import pytesseract
import numpy as np
import sys
import getopt


print ("Number of arguments:", len(sys.argv), "arguments.")

print ("Argument List:", str(sys.argv))

inputfile = ''
outputfile = ''
try:
  opts, args = getopt.getopt(sys.argv,"hi:o:",["ifile=","ofile="])
except getopt.GetoptError:
  print( 'test.py -i <inputfile> -o <outputfile>')
  sys.exit(2)
for opt, arg in opts:
   if opt == '-h':
      print( 'test.py -i <inputfile> -o <outputfile>')
      sys.exit()
   elif opt in ("-i", "--ifile"):
      inputfile = arg
   elif opt in ("-o", "--ofile"):
      outputfile = arg

print('Input file is "', inputfile)
print('Output file is "', outputfile)

url = inputfile

img = cv2.imread(".+url")                       #Alternatively: can be skipped if you have a Blackwhite image
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
gray, img_bin = cv2.threshold(gray,128,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
gray = cv2.bitwise_not(img_bin)


kernel = np.ones((2, 1), np.uint8)
img = cv2.erode(gray, kernel, iterations=1)
img = cv2.dilate(img, kernel, iterations=1)
out_below = pytesseract.image_to_string(img)
print("OUTPUT:", out_below)
