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


class ObjectList:
    X = None
    Y = None
    W = None
    H = None
    Type = None


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


##TODO
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
    #implied param, return: w - width of the template
    #implied param, return: h - height of the template
    #implied param, return: type - reference of list of types of found objects
    #return first - boolean if list is found
def iterateResource(X, Y, type, w, h, name, objType, threshold, first, left = 0, top = 0, src = img_gray, dst = img_sheet_music):
#    files_list = glob.glob('/resources/')

    for file in files_list:
        template = cv2.imread(file, 0)
        (tw, th) = template.shape[::-1]
        first = findObjects(X, Y, type, tw, th, objType, template, threshold, first, left, top, dst = out)

    return first

#function findStaffLines checks pixels along the X axis for each Y value and finds
#the lines with the most amount of black pixels.
    #param img_src - img to use as source for finding lines
    #param img_display - img to display found lines on
    #return: lines - list of lines with black pixel values over 1000.
def findStaffLines(img_src = img_gray, img_display = img_sheet_music):
    #step 1: preprocessing/Staff Lines
        #identifying and removing staff bars in order to clarify image
        #removing staff bars is optional. TODO: find way to remove spaces without
        #compromising quality after removing bars
    lines = []
    for i in range(2200):
        count = 0
        for j in range(1700):
            if img_gray[i, j] < 200:
                count += 1
        #print("row", i, ":", count)
        cv2.line(img_sheet_music, (0,i), (count, i), (255, 0, 0), 1)
        #if line is found, add to list
        if count > 1000:
            lines.append(i)
    #remove lines that are duplicate within row range (too close to each other - within 8 pixels)
    slines = []
    for idx in range(0, len(lines)):
        if abs(lines[idx]-lines[idx-1]) > 8:
            slines.append(lines[idx])
            cv2.line(img_sheet_music, (0,lines[idx]), (100, lines[idx]), (0, 0, 255), 2)
    cv2.putText(img_sheet_music, 'Staff Lines', (35, 20), font, .5, (0, 0, 255), 2)
    return slines

#main
#instantiate object properties to empty lists
Objects = ObjectList()
Objects.X = []
Objects.Y = []
Objects.W = []
Objects.H = []
Objects.Type = []

#step 1 - staff line recognition
staffLines = findStaffLines()

#step 2 - object recognition
#1 - note_head, 2 - hollow_note_head, 3 - sharp, 4 - flat, 5 - natural, 6 - whole_rest
#7 - half_rest, 8 - quarter_rest, 9 - eighth_rest, 10 - sixteenth_rest, 11 - dot
#-1 - treble_clef, -2 - base_clef
first = True
#find full note heads
name = "head_full"
objType = 1
threshold = .9
first = iterateResource(X, Y, Type, W, H, name, objType, threshold, first, )
