#!/usr/bin/python3
#Author: Matthew Yu
#templateTest.py
#as of 5/6/18, template currently matches solid note heads of Accumula Town and
#Floaroma Town with an acc around ~95%.
#TODO: adjust threshold for best results, test with more sheet music
#add hollow notes, dots to identify whole notes, dotted notes
#begin horizontal line checking to start assessing pitch
#begin merging with readSheetMusV1/V2.py

import cv2
import numpy as np

MAX_CENTERS = 100

sheetname = "Accumula_Town" #"Floaroma_Town"

img_sheet_music = cv2.imread(sheetname + '.jpg')

#if wrong size, resize
shape = np.shape(img_sheet_music)
if shape[0] != 1700 or shape[1] != 2200:
    img_sheet_music = cv2.resize(img_sheet_music, (1700, 2200)) #width, height

img_gray = cv2.cvtColor(img_sheet_music, cv2.COLOR_BGR2GRAY)
#note_head
template = cv2.imread('empty_note_head.png', 0)
w, h = template.shape[::-1]
#empty_note_head
template2 = cv2.imread('empty_note_head.png', 0)
w2, h2 = template2.shape[::-1]

#empty 2d array for (X,Y)
X = []
Y = []
first = True
key = True

res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
threshold = 0.72
loc = np.where( res >= threshold)
if loc is not None:
    for pt in sorted(zip(*loc[::-1]), key = lambda x:x[0]):
        #for each pt determine center, compare to within range of other centers
        #get (X,Y)
        nX = pt[0]
        nY = pt[1]
        #print(pt)
        ##if first entry
        if first is True:
            X.append(nX)
            Y.append(nY)
            cv2.rectangle(img_sheet_music, pt, (nX + w, nY + h), (0, 0, 255), 2)
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
                #if in range, ignore, else draw
                cv2.rectangle(img_sheet_music, pt, (nX + w, nY + h), (0, 0, 255), 1)


#for coords in zip(X, Y):
#    print(coords)

cv2.imshow("res", img_sheet_music)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite(sheetname + '2.png', img_sheet_music)
