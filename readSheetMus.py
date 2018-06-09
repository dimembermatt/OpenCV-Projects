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
#readSheetMus.py

import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('fragment2.jpg', cv2.IMREAD_GRAYSCALE)
shape = np.shape(img)
#if too big, resize
if shape[0] > 700 or shape[1] > 900:
    img = cv2.resize(img, (700, 900)) #width, height

#img = cv2.resize(img, (0, 0), fx = 2, fy = 2)

#get threshold
#ret, mask = cv2.threshold(img, 185, 255, cv2.THRESH_BINARY)

#clean image to only outlines
canny = cv2.Canny(img, 20, 60)
#get color editable images for related sections
staff = cv2.cvtColor(canny, cv2.COLOR_GRAY2BGR)
notes = cv2.cvtColor(canny, cv2.COLOR_GRAY2BGR)


#find staff bar with HoughLines
#lines = cv2.HoughLinesP(canny, 1, np.pi/180, threshold = 400, minLineLength=50, maxLineGap=100)    #for sheetmus.jpg
lines = cv2.HoughLinesP(canny, 1, np.pi/180, threshold = 20, minLineLength=200, maxLineGap=130)       #for fragment2.jpg
#print(lines)
topLineY = botLineY = lines[0][0][1]
idx = idx2 = 0
for i in range(0, len(lines)):
    x1, y1, x2, y2 = lines[i][0]
    if (y2-y1) == 0:  #only print horizontal lines
        cv2.line(staff, (x1, y1), (x2, y2), (0,0,255), 1, cv2.LINE_AA)
        #find top line bound
        if y1 < topLineY:
            topLineY = y1
            idx = i
        #find bottom line bound
        if y1 > botLineY:
            botLineY = y1
            idx2 = i
#print(topLineY, idx, botLineY, idx2)

#overlay top line, bottom line
cv2.line(staff, (lines[idx][0][0], lines[idx][0][1]), (lines[idx][0][2], lines[idx][0][3]), (0,255,0), 1, cv2.LINE_AA)
cv2.line(staff, (lines[idx2][0][0], lines[idx2][0][1]), (lines[idx2][0][2], lines[idx2][0][3]), (0,255,0), 1, cv2.LINE_AA)
#get new area
roi = staff[lines[idx][0][1] - 14:lines[idx2][0][1] + 14, lines[idx][0][0]:lines[idx][0][2]]

canny = cv2.Canny(roi, 20, 60)
#find note heads with HoughCircles

#working up to HERE - still trying to get HoughCircles working.
#consider switching to just contour finding
accThresh = 1000
cannyThresh = 20
minRad = 6
maxRad = 3*minRad - 1
minDist = 300
dp = 1
i = 0
while i < 15:
    print("Working on sample" + str(i))
    notes = cv2.cvtColor(canny, cv2.COLOR_GRAY2BGR)
    circles = cv2.HoughCircles(canny, cv2.HOUGH_GRADIENT, dp, minDist, cannyThresh, accThresh, minRad, maxRad)
    if circles is not None:
        circles = np.round(circles[0, :].astype("int"))
        print(circles)
        for (x, y, r) in circles:
            cv2.circle(notes, (x, y), 10, (255, 0, 0), 2)
            cv2.circle(notes, (x, y), 10, (0, 0, 255), 3)

    cv2.imwrite('sample' + str(i) + '.jpg', notes)

    accThresh += 30
    i += 1


cv2.imshow('orig', img)
cv2.imshow('staff', staff)
cv2.imshow('noteheads', notes)
cv2.waitKey(0)
cv2.destroyAllWindows()
#cv2.imwrite('Accumula Town-1_s.jpg', img)
