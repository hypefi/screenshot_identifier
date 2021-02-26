import cv2
from pathlib import Path
import pytesseract
import numpy as np
import sys
import getopt
import os
#import proselint
import re
from autocorrect import Speller
from spellchecker import SpellChecker

spell_l2 = SpellChecker()
spell = Speller()

#print ("Number of arguments:", len(sys.argv), "arguments.")
#print ("Argument List:", str(sys.argv))

directory_in_str = sys.argv[1]

pathlist = Path(directory_in_str).glob('**/*.png')

#spell checker 2
WORD = re.compile(r'\w+')

def reTokenize(doc):
    tokens = WORD.findall(doc)
    return tokens

def spell_correct(text):
    sptext =  [' '.join([spell_l2.correction(w).lower() for w in reTokenize(doc)])  for doc in text]
    return sptext
#end of spell checker 2 

def change_name(url):
    print(url)

    img = cv2.imread(url)                       #Alternatively: can be skipped if you have a Blackwhite image
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray, img_bin = cv2.threshold(gray,128,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    gray = cv2.bitwise_not(img_bin)


    kernel = np.ones((2, 1), np.uint8)
    img = cv2.erode(gray, kernel, iterations=1)
    img = cv2.dilate(img, kernel, iterations=1)
    out_below = pytesseract.image_to_string(img)
    #print("OUTPUT:", out_below)

    #linter - with proselint not working yet 

    #suggestions = proselint.tools.lint(out_below)
    #print("suggestions ", suggestions)

    #change file name from title

    path = os.path.dirname(url)
    #print(path)
    #spell check lv1
    corrected = spell(out_below)
    #spell check lv2
    #corrected_2 = spell_correct(corrected)
    #print("corrected2", corrected_2)
    #corr = ''

    #corr.join(corrected_2)
    #print("corr", corr)
    #replacing ? with space 
    corrected = ' '.join(corrected.split())
    #print("correct3" , corrected_3)

    newfilename = path + "/" + corrected + ".png"
    print("url", url)
    print("newfilename", newfilename)
    try:
        os.rename(url,newfilename)
    except OSError:
        nfilename = corrected + ".png"
        newfilename = path + "/" + re.sub('[!@#>/\<~]', '', corrected)
        os.rename(url,newfilename[0:180])
    finally:
        pass

for path in pathlist:
     path_in_str = str(path)
     print(path_in_str)
     change_name(path_in_str)
