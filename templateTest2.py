#!/usr/bin/python3
#Author: Matthew Yu
#templateTestq.py

#V2 - implementation of resource folder with template elements categorized in order
#to raise threshold accuracy of template matching

#history:
    #as of 6/6/18, template currently matches solid note heads of Accumula Town and
    #Floaroma Town with an acc around ~95%.
    #as of 6/8/18, template matches solid note heads, hollow note heads, sharps, flats,
    #and naturals, as well as full size clefs with good accuracy
    #naturals can tend to be found accidentally in unexpected places.

#TODO: adjust threshold for best results, test with more sheet music
    #add rests, dots, classify staff separation
    #begin horizontal line checking to start assessing pitch
    #begin merging with readSheetMusV1/V2.py

import cv2
import numpy as np
import glob
import copy

font = cv2.FONT_HERSHEY_SIMPLEX

def nothing(x):
    pass

#init
sheetname = "SS_Anne"#"Floaroma_Town"#"Accumula_Town" #
img_sheet_music = cv2.imread(sheetname + '.jpg')

#if wrong size, resize
shape = np.shape(img_sheet_music)
if shape[0] != 1700 or shape[1] != 2200:
    img_sheet_music = cv2.resize(img_sheet_music, (1700, 2200)) #width, height
#canvas program uses to determine objects
img_gray = cv2.cvtColor(img_sheet_music, cv2.COLOR_BGR2GRAY)

#function findObjects takes a template and attempts to find a list of locations of
#objects that match the template in an image.
    #param: w - width of the template
    #param: h - height of the template
    #param: objType - identifier for objType
    #param: template - template object to find
    #param: threshold - change threshold value to affect how well object is found
    #param: first - boolean run through each pass to determine if lists are found
    #optional param: left - leftmost position to identify objects
    #optional param: top - topmost position to identify objects
    #optional param: src - image source to find objects
    #optional param: dst - image dst to display found objects
    #implied param, return: X - reference of list of X coordinates of found objects
    #implied param, return: Y - reference of list of Y coordinates of found objects
    #implied param, return: type - reference of list of types of found objects
    #return first - boolean if list is found
def findObjects(X, Y, type, w, h, objType, template, threshold, first, left = 0, top = 0, src = img_gray, dst = img_sheet_music):
    #get location of object
    res = cv2.matchTemplate(src, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where( res >= threshold)

    if loc is not None:
        for pt in sorted(zip(*loc[::-1]), key = lambda x:x[0]):
            #for each pt determine center, compare to within range of other centers
            #get (X,Y)
            nX = pt[0]
            nY = pt[1]
            if nX > left and nY > top - 10:
                #if first entry
                if first is True:
                    X.append(nX)
                    Y.append(nY)
                    type.append(objType)
                    cv2.rectangle(dst, pt, (nX + w, nY + h), (255, 0, 0), 2)
                    first = False
                #if not first entry
                else:
                    #go through X and Y, and check dist
                    key = True
                    for coord in zip(X, Y):
                        #if too close in X or Y dir, exclude; else add to arr and draw
                        dX = abs(coord[0] - nX)
                        dY = abs(coord[1] - nY)
                        if dX < 10 and dY < 10:
                            key = False
                            break

                    if key is True:
                        X.append(nX)
                        Y.append(nY)
                        type.append(objType)
                        #if in range, ignore, else draw
                        cv2.rectangle(dst, pt, (nX + w, nY + h), (255, 0, 0), 1)
    return first

#function iterateResource takes in a name of folder (found in resources) and iterates
#findObjects for every template image in the folder.
    #param: name of folder
    #param: objType - identifier for objType
    #param: threshold - change threshold value to affect how well object is found
    #param: first - boolean run through each pass to determine if lists are found
    #optional param: left - leftmost position to identify objects
    #optional param: top - topmost position to identify objects
    #optional param: src - image source to find objects
    #optional param: dst - image dst to display found objects
    #implied param, return: X - reference of list of X coordinates of found objects
    #implied param, return: Y - reference of list of Y coordinates of found objects
    #implied param, return: type - reference of list of types of found objects
    #return first - boolean if list is found
    def iterateResource(X, Y, type, name, objType, threshold, first, left = 0, top = 0, src = img_gray, dst = img_sheet_music):
#    files_list = glob.glob('/resources/')

    for file in files_list:
        template = cv2.imread(file, 0)
        (tw, th) = template.shape[::-1]
        first = findObjects(X, Y, type, tw, th, objType, template, threshold, first, left, top, dst = out)

    return first    
