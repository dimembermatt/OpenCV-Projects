#!/usr/bin/python3
#Author: Matthew Yu
#templateTest.py

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

MAX_CENTERS = 100
font = cv2.FONT_HERSHEY_SIMPLEX

#function findObjects takes a template and attempts to find a list of locations of
#objects that match the template in an image.
    #param: w - width of the template
    #param: h - height of the template
    #param: template - template object to find
    #param: threshold - change threshold value to affect how well object is found
    #param: first - boolean run through each pass to determine if lists are found
    #optional param: left - leftmost position to identify objects
    #optional param: top - topmost position to identify objects
    #implied param, return: X - reference of list of X coordinates of found objects
    #implied param, return: Y - reference of list of Y coordinates of found objects
    #implied param, return: type - reference of list of types of found objects
def findObjects(X, Y, type, w, h, objType, template, threshold, first, left = 0, top = 0):
    #get location of object
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where( res >= threshold)

    if loc is not None:
        for pt in sorted(zip(*loc[::-1]), key = lambda x:x[0]):
            #for each pt determine center, compare to within range of other centers
            #get (X,Y)
            nX = pt[0]
            nY = pt[1]
            if nX > left and nY > top:
                #if first entry
                if first is True:
                    X.append(nX)
                    Y.append(nY)
                    type.append(objType)
                    cv2.rectangle(img_sheet_music, pt, (nX + w, nY + h), (255, 0, 0), 2)
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
                        cv2.rectangle(img_sheet_music, pt, (nX + w, nY + h), (255, 0, 0), 1)
    return first

#init
sheetname = "Floaroma_Town"#"Accumula_Town" #
img_sheet_music = cv2.imread(sheetname + '.jpg')

#if wrong size, resize
shape = np.shape(img_sheet_music)
if shape[0] != 1700 or shape[1] != 2200:
    img_sheet_music = cv2.resize(img_sheet_music, (1700, 2200)) #width, height
#canvas program uses to determine objects
img_gray = cv2.cvtColor(img_sheet_music, cv2.COLOR_BGR2GRAY)

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

#remove lines that are duplicate within row range
slines = []
for idx in range(0, len(lines)):
    if abs(lines[idx]-lines[idx-1]) > 8:
        slines.append(lines[idx])
        cv2.line(img_sheet_music, (0,lines[idx]), (100, lines[idx]), (0, 0, 255), 2)
lines = slines
cv2.putText(img_sheet_music, 'Staff Lines', (35, 20), font, .5, (0, 0, 255), 2)
#print(lines)

#step 2: object recognition
    #identify note head types, note tail types, accidentals, clefs, staff signatures,
    #dots which indicate dotted notes, etc, key signatures, time signatures.
treble = cv2.imread('treble_clef.png', 0)
tw, th = treble.shape[::-1]
base = cv2.imread('base_clef.png', 0)
bw, bh = base.shape[::-1]
#note_head
note_head = cv2.imread('note_head.png', 0)
w1, h1 = note_head.shape[::-1]
#empty_note_head
h_note_head = cv2.imread('hollow_note_head.png', 0)
w2, h2 = h_note_head.shape[::-1]
#sharp
sharp = cv2.imread('sharp.png', 0)
w3, h3 = sharp.shape[::-1]
#flat
flat = cv2.imread('flat.png', 0)
w4, h4 = flat.shape[::-1]
#natural
natural = cv2.imread('natural.png', 0)
w5, h5 = natural.shape[::-1]
#whole_rest
whole_rest = cv2.imread('whole_rest.png', 0)
w6, h6 = whole_rest.shape[::-1]
#half_rest
half_rest = cv2.imread('half_rest.png', 0)
w7, h7 = half_rest.shape[::-1]
#quarter_rest
quarter_rest = cv2.imread('quarter_rest.png', 0)
w8, h8 = quarter_rest.shape[::-1]
#eighth_rest
eighth_rest = cv2.imread('eighth_rest.png', 0)
w9, h9 = eighth_rest.shape[::-1]
#sixteenth_rest
sixteenth_rest = cv2.imread('sixteenth_rest.png', 0)
w10, h10 = sixteenth_rest.shape[::-1]
#dot
dot = cv2.imread('dot.png', 0)
w11, h11 = dot.shape[::-1]

#empty 2d array for (X,Y) coordinates of all objects
X = []
Y = []
#1 - note_head, 2 - hollow_note_head, 3 - sharp, 4 - flat, 5 - natural, 6 - whole_rest
#7 - half_rest, 8 - quarter_rest, 9 - eighth_rest, 10 - sixteenth_rest, 11 - dot
#-1 - treble_clef, -2 - base_clef
type = []
first = True
key = True

#get location of treble_clef
first = findObjects(X, Y, type, tw, th, -1, treble, 0.60, first)
#get location of base_clef
first = findObjects(X, Y, type, bw, bh, -2, base, 0.60, first)

#get top left most corner to sort
left = X[0] + tw
top  = Y[0]
for coord in zip(X, Y, type):
    if coord[2] is 5:
        if coord[0] + tw < left:
            left = coord[0] + tw
    elif coord[2] is 6:
        if coord[0] + bw < left:
            left = coord[0] + bw
    if coord[1] < top:
        top = coord[1]

cv2.putText(img_sheet_music, 'Corner', (left, top), font, .5, (0, 0, 255), 2)
#print("left:", left)
#print("top:", top)

#get location of note_heads
first = findObjects(X, Y, type, w1, h1, 1, note_head, 0.72, first, left, top)
#get location of hollow_note_heads
first = findObjects(X, Y, type, w2, h2, 2, h_note_head, 0.58, first, left, top)
#get location of whole_rest
first = findObjects(X, Y, type, w6, h6, 6, whole_rest, 0.93, first, left, top)
#get location of half_rest
#first = findObjects(X, Y, type, w7, h7, 7, half_rest, 0.85, first, left, top)
#get location of quarter_rest
first = findObjects(X, Y, type, w8, h8, 8, quarter_rest, 0.85, first, left, top)
#get location of eighth_rest
#first = findObjects(X, Y, type, w9, h9, 9, eighth_rest, 0.85, first, left, top)
#get location of sixteenth_rest
#first = findObjects(X, Y, type, w10, h10, 10, sixteenth_rest, 0.85, first, left, top)
#get location of sharps
#first = findObjects(X, Y, type, w3, h3, 3, sharp, 0.67, first, left, top)
#get location of flats
#first = findObjects(X, Y, type, w4, h4, 4, flat, 0.70, first, left, top)
#get location of naturals
#first = findObjects(X, Y, type, w5, h5, 5, natural, 0.72, first, left, top)
#get location of dots

#step 3: determine pitches
    #use staff lines to determine note pitches and subdivide notes into sections
    #based on division of staff bar groups

#display output of processes occuring to the sheetmusic
#write centerpoint dot for each note_head as well as type
#0 - note_head, 1 - hollow_note_head, 2 - sharp, 3 - flat, 4 - natural, 5 - treble_clef, 6 - base_clef
centers = []
for coord in zip(X, Y, type):
    if coord[2] is 1:
        donothing = 0
        cv2.putText(img_sheet_music, 'Q/E/S', (coord[0], coord[1]), font, .5, (0, 0, 255), 2)
        cv2.circle(img_sheet_music, (int(coord[0] + w1/2), int(coord[1] + h1/2)), 2, (255, 0, 0))
    if coord[2] is 2:
        cv2.putText(img_sheet_music, 'W/H', (coord[0], coord[1]), font, .5, (0, 0, 255), 2)
        cv2.circle(img_sheet_music, (int(coord[0] + w2/2), int(coord[1] + h2/2)), 2, (255, 0, 0))
    if coord[2] is 3:
        cv2.putText(img_sheet_music, 'Sharp', (coord[0], coord[1]), font, .5, (255, 0, 0), 2)
    if coord[2] is 4:
        cv2.putText(img_sheet_music, 'Flat', (coord[0], coord[1]), font, .5, (255, 0, 0), 2)
    if coord[2] is 5:
        cv2.putText(img_sheet_music, 'Natural', (coord[0], coord[1]), font, .5, (255, 0, 0), 2)
    if coord[2] is 6:
        cv2.putText(img_sheet_music, 'WR', (coord[0], coord[1]), font, .5, (0, 255, 0), 2)
    if coord[2] is 7:
        cv2.putText(img_sheet_music, 'HR', (coord[0], coord[1]), font, .5, (0, 255, 0), 2)

cv2.imshow("res", img_sheet_music)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite(sheetname + '2.png', img_sheet_music)
