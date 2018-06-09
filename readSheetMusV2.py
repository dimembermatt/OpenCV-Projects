#!/usr/bin/python3
#Author: Matthew Yu
#Created: 5/23/2018
#Version 1.0 - 5/23/18
#TODO: get basic functionality, then set to ask for input (a folder name with
#all the sheet music of a specific song in jpg form) and program reads all jpgs
#as a single file.
#
#This program takes a jpg image of a music sheet and attempts to read it using
#openCV. Elements such as staff, key, tempo, and notes are recorded and an array
#containing the elements are formatted into a text file that can be read by
#TivaBoy's MusicBox in order to play music.
#
#VERSION2: This version attempts to first detect staff bars and notes separate
#from eac other.
#
#readSheetMusV2.py

import numpy as np
import cv2
from matplotlib import pyplot as plt

def blob_Detect(im, circularity, min_area, convexity, inertia):
    #set params
    params = cv2.SimpleBlobDetector_Params()
    # Change thresholds
    params.minThreshold = 10
    params.maxThreshold = 200

    # Filter by Area.
    params.filterByArea = True
    params.minArea = min_area

    # Filter by Circularity
    params.filterByCircularity = True
    params.minCircularity = circularity

    # Filter by Convexity
    params.filterByConvexity = True
    params.minConvexity = convexity

    # Filter by Inertia
    params.filterByInertia = True
    params.minInertiaRatio = inertia
    #detect
    detector = cv2.SimpleBlobDetector_create(params)
    keypoints = detector.detect(im)
    #print(keypoints)
    noteheads_f = cv2.drawKeypoints(im, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    return noteheads_f


#start
img = cv2.imread('fragment2.jpg', cv2.IMREAD_GRAYSCALE)
shape = np.shape(img)
print(shape)
#if too big, resize
if shape[0] > 700 or shape[1] > 900:
    img = cv2.resize(img, (700, 900)) #width, height

imgA = cv2.bitwise_not(img)
ret, imgA = cv2.threshold(imgA, 80, 255, cv2.THRESH_BINARY)
staff = np.copy(imgA)
notes = np.copy(imgA)

#get horizontal staff bars
cols = staff.shape[1]
horizontal_size = int(cols/3)#int(cols/30)
horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_size, 1))
staff = cv2.erode(staff, horizontalStructure)
staff = cv2.dilate(staff, horizontalStructure)

#get notes from staff bars
ret, staff = cv2.threshold(staff, 80, 255, cv2.THRESH_BINARY)
ret, notes = cv2.threshold(notes, 80, 255, cv2. THRESH_BINARY)
notes = cv2.bitwise_xor(staff, notes, True)

fillStructure = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4))
notes = cv2.morphologyEx(notes, cv2.MORPH_CLOSE, fillStructure)

#find noteheads using blob detector
noteheads = cv2.cvtColor(notes, cv2.COLOR_GRAY2BGR)
notesInv = cv2.bitwise_not(notes)
font = cv2.FONT_HERSHEY_SIMPLEX
i = circularity = 0
while circularity < 1:
    min_area = 1
    while min_area < 500:
        convexity = 0
        while convexity < 1:
            inertia = 0
            while inertia < 1:
                print("working on sample", i)
                noteheads_f = blob_Detect(notesInv, circularity, min_area, convexity, inertia)
                cv2.imwrite('sample' + str(i) + '_ci' + str(circularity) + '_ar' + str(min_area) + '_co' + str(convexity) + '_in' + str(inertia) + '.jpg', noteheads_f)
                i += 1

                inertia += .2
            convexity += .2
        min_area += 25
    circularity += .2


#cv2.imshow('orig', imgA)
#cv2.imshow('staff', staff)
#cv2.imshow('notes', notes)
#cv2.imshow('noteheads', noteheads)
#cv2.imshow('noteheads_found', noteheads_f)
#cv2.waitKey(0)
print("done")
cv2.destroyAllWindows()
