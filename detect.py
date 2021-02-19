import cv2
from pathlib import Path
import pytesseract
import numpy as np
import sys
import getopt
import os
import proselint
from autocorrect import Speller
spell = Speller()

print ("Number of arguments:", len(sys.argv), "arguments.")

print ("Argument List:", str(sys.argv))

directory_in_str = sys.argv[1]

pathlist = Path(directory_in_str).glob('**/*.png')



#url = "." + sys.argv[1]

def change_name(url):
    print("Hello from a function")
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
    suggestions = proselint.tools.lint(out_below)
    print("suggestions ", suggestions)
    #change file name from title

    path = os.path.dirname(url)
    #print(path)
    corrected = spell(out_below)
    #replacing ? with space 
    corrected = ' '.join(corrected.split())


    newfilename = path + "/" + corrected + ".png"
    print(newfilename)
    try:
        os.rename(url,newfilename)
    except OSError:
        os.rename(url,newfilename[0:150])

for path in pathlist:
     # because path is object not string
     path_in_str = str(path)
     print(path_in_str)
     change_name(path_in_str)
