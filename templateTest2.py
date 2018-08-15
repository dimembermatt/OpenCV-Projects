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
sheetname = "./sheet_music/Goldenrod City"#"Floaroma_Town"#"Accumula_Town" #
img_sheet_music = cv2.imread(sheetname + '.jpg')

#if wrong size, resize
shape = np.shape(img_sheet_music)
if shape[0] != 1700 or shape[1] != 2200:
    img_sheet_music = cv2.resize(img_sheet_music, (1700, 2200)) #width, height
#canvas program uses to determine objects
img_gray = cv2.cvtColor(img_sheet_music, cv2.COLOR_BGR2GRAY)
img_out = copy.copy(img_sheet_music)

#function findObjects takes a template and attempts to find a list of locations of
#objects that match the template in an image.
    #param: tw - width of the template
    #param: th - height of the template
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
    #implied param, return: W - reference of list of Widths of found objects
    #implied param, return: H - reference of list of Heights of found objects
    #implied param, return: type - reference of list of types of found objects
    #return first - boolean if list is found
def findObjects(X, Y, type, W, H, tw, th, objType, template, threshold, first, left = 0, top = 0, src = img_gray, dst = img_out):
    #get location of object
    res = cv2.matchTemplate(src, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where( res >= threshold)

    if loc is not None:
        for pt in sorted(zip(*loc[::-1]), key = lambda x:x[0]):
            #for each pt determine center, compare to within range of other centers
            #get (X,Y)
            nX = pt[0]
            nY = pt[1]
            nType = objType
            if nX > left and nY > top - 10:
                #if first entry
                if first is True:
                    X.append(nX)
                    Y.append(nY)
                    W.append(tw)
                    H.append(th)
                    type.append(objType)
                    #cv2.rectangle(dst, pt, (nX + tw, nY + th), (255, 0, 0), 2)
                    first = False
                #if not first entry
                else:
                    #go through X and Y, and check dist
                    key = True
                    for coord in zip(X, Y, W, H, type):
                        #if too close in X or Y dir, exclude; else add to arr and draw
                        ###if coord[2] == nType :
                        dX = abs((coord[0] + coord[2]/2) - (nX + tw/2))
                        dY = abs((coord[1] + coord[3]/2) - (nY + th/2))
                        if dX < 10 and dY < 10 and nType == coord[4]:
                            key = False
                            break

                    if key is True:
                        X.append(nX)
                        Y.append(nY)
                        W.append(tw)
                        H.append(th)
                        type.append(objType)
                        #if in range, ignore, else draw
                        #cv2.rectangle(dst, pt, (nX + tw, nY + th), (255, 0, 0), 1)
    return first


##TODO - test independently
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
    #implied param, return: W - reference of list of Widths of found objects
    #implied param, return: H - reference of list of Heights of found objects
    #implied param, return: type - reference of list of types of found objects
    #return first - boolean if list is found
def iterateResource(X, Y, type, W, H, name, objType, threshold, first, left = 0, top = 0, src = img_gray, dst = img_out):
    for file in glob.glob('./resources/' + name + '/*.png'):
        template = cv2.imread(file, 0)
        tw, th = template.shape[::-1]
        first = findObjects(X, Y, type, W, H, tw, th, objType, template, threshold, first, left, top, src, dst)
    return first

#function findStaffLines checks pixels along the X axis for each Y value and finds
#the lines with the most amount of black pixels.
    #param img_src - img to use as source for finding lines
    #param img_display - img to display found lines on
    #return: lines - list of lines with black pixel values over 1000.
def findStaffLines(img_src = img_gray, img_display = img_out):
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
            cv2.line(img_display, (0,lines[idx]), (100, lines[idx]), (0, 0, 255), 2)
    cv2.putText(img_display, 'Staff Lines', (35, 20), font, .5, (0, 0, 255), 2)
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
img = np.zeros((10, 800, 3), np.uint8)
cv2.namedWindow('image')
cv2.namedWindow('img_out', cv2.WINDOW_NORMAL)
# create trackbars for color change
cv2.createTrackbar('full_NH','image', 0, 100, nothing)
cv2.createTrackbar('hollow_NH','image', 0, 100, nothing)
cv2.createTrackbar('whole_NH','image', 0, 100, nothing)
cv2.createTrackbar('sharp','image', 0, 100, nothing)
cv2.createTrackbar('flat','image', 0, 100, nothing)
cv2.createTrackbar('natural','image', 0, 100, nothing)
cv2.createTrackbar('WR','image', 0, 100, nothing)
cv2.createTrackbar('HR','image', 0, 100, nothing)
cv2.createTrackbar('QR','image', 0, 100, nothing)
cv2.createTrackbar('ER','image', 0, 100, nothing)
cv2.createTrackbar('SR','image', 0, 100, nothing)
cv2.createTrackbar('dot','image', 0, 100, nothing)
cv2.createTrackbar('repeat','image', 0, 100, nothing)
cv2.createTrackbar('repeat_end','image', 0, 100, nothing)
cv2.createTrackbar('base_clef','image', 0, 100, nothing)
cv2.createTrackbar('treble_clef','image', 0, 100, nothing)
iteration = 0
while(1):
    cv2.imshow('image', img)
    k = cv2.waitKey(0) & 0xFF
    if k == 27:
        break;
    print("running")
    iteration += 1

    #step 2 - object recognition
    #0 - note_head, 1 - hollow_note_head, 2 - whole_note 3 - sharp, 4 - flat, 5 - natural, 6 - whole_rest
    #7 - half_rest, 8 - quarter_rest, 9 - eighth_rest, 10 - sixteenth_rest, 11 - dot, 12 - repeat, 13 - repeat_end
    #-1 - base_clef, -2 - treble_clef
    first = True

    Objects.X = []
    Objects.Y = []
    Objects.W = []
    Objects.H = []
    Objects.Type = []
    img_out = copy.copy(img_sheet_music)
    cv2.putText(img_out, str(iteration), (1600, 100), font, 2, (0, 0, 255), 2)


    #TODO: calculate top and left (and/or bottom) for each staff line group and use as left/top
    #find full note heads
    name = "head_full"
    objType = 0
    threshold = cv2.getTrackbarPos('full_NH','image')/100
    first = iterateResource(Objects.X, Objects.Y, Objects.Type, Objects.W, Objects.H, name, objType, threshold, first, )
    #find hollow note heads
    name = "head_hollow"
    objType = 1
    threshold = cv2.getTrackbarPos('hollow_NH','image')/100
    first = iterateResource(Objects.X, Objects.Y, Objects.Type, Objects.W, Objects.H, name, objType, threshold, first, )
    #find whole note notes
    name = "head_whole"
    objType = 2
    threshold = cv2.getTrackbarPos('whole_NH','image')/100
    first = iterateResource(Objects.X, Objects.Y, Objects.Type, Objects.W, Objects.H, name, objType, threshold, first, )
    #find sharps
    name = "accidental_sharp"
    objType = 3
    threshold = cv2.getTrackbarPos('sharp','image')/100
    first = iterateResource(Objects.X, Objects.Y, Objects.Type, Objects.W, Objects.H, name, objType, threshold, first, )
    #find flats
    name = "accidental_flat"
    objType = 4
    threshold = cv2.getTrackbarPos('flat','image')/100
    first = iterateResource(Objects.X, Objects.Y, Objects.Type, Objects.W, Objects.H, name, objType, threshold, first, )
    #find naturals
    name = "accidental_natural"
    objType = 5
    threshold = cv2.getTrackbarPos('natural','image')/100
    first = iterateResource(Objects.X, Objects.Y, Objects.Type, Objects.W, Objects.H, name, objType, threshold, first, )
    #find whole rests
    name = "rest_whole"
    objType = 6
    threshold = cv2.getTrackbarPos('WR','image')/100
    first = iterateResource(Objects.X, Objects.Y, Objects.Type, Objects.W, Objects.H, name, objType, threshold, first, )
    #find half rests
    name = "rest_half"
    objType = 7
    threshold = cv2.getTrackbarPos('HR','image')/100
    first = iterateResource(Objects.X, Objects.Y, Objects.Type, Objects.W, Objects.H, name, objType, threshold, first, )
    #find quarter rests
    name = "rest_quarter"
    objType = 8
    threshold = cv2.getTrackbarPos('QR','image')/100
    first = iterateResource(Objects.X, Objects.Y, Objects.Type, Objects.W, Objects.H, name, objType, threshold, first, )
    #find eighth rests
    name = "rest_eighth"
    objType = 9
    threshold = cv2.getTrackbarPos('ER','image')/100
    first = iterateResource(Objects.X, Objects.Y, Objects.Type, Objects.W, Objects.H, name, objType, threshold, first, )
    #find sixteenth rests
    name = "rest_sixteenth"
    objType = 10
    threshold = cv2.getTrackbarPos('SR','image')/100
    first = iterateResource(Objects.X, Objects.Y, Objects.Type, Objects.W, Objects.H, name, objType, threshold, first, )
    #find dot
    # name = "dot"
    # objType = 11
    # threshold = cv2.getTrackbarPos('dot','image')/100
    # first = iterateResource(Objects.X, Objects.Y, Objects.Type, Objects.W, Objects.H, name, objType, threshold, first, )
    #find repeat
    name = "repeat"
    objType = 12
    threshold = cv2.getTrackbarPos('repeat','image')/100
    first = iterateResource(Objects.X, Objects.Y, Objects.Type, Objects.W, Objects.H, name, objType, threshold, first, )
    #find repeat ends
    name = "repeat_end"
    objType = 13
    threshold = cv2.getTrackbarPos('repeat_end','image')/100
    first = iterateResource(Objects.X, Objects.Y, Objects.Type, Objects.W, Objects.H, name, objType, threshold, first, )
    #find base clef
    name = "clef_base"
    objType = -1
    threshold = cv2.getTrackbarPos('base_clef','image')/100
    first = iterateResource(Objects.X, Objects.Y, Objects.Type, Objects.W, Objects.H, name, objType, threshold, first, )
    #find treble clef
    name = "clef_treble"
    objType = -2
    threshold = cv2.getTrackbarPos('treble_clef','image')/100
    first = iterateResource(Objects.X, Objects.Y, Objects.Type, Objects.W, Objects.H, name, objType, threshold, first, )

    print("Xcoord len: ", len(Objects.X))
    print("Ycoord len: ", len(Objects.Y))
    print("Width len: ", len(Objects.W))
    print("Height len: ", len(Objects.H))
    print("Type len: ", len(Objects.Type))

    #display output of processes occuring to the sheetmusic
    #write centerpoint dot for each note_head as well as type
    for coord in zip(Objects.X, Objects.Y, Objects.W, Objects.H, Objects.Type):
        if coord[4] is -2:
            cv2.putText(img_out, 'T_C', (coord[0], coord[1]), font, .5, (0, 0, 255), 2)
            cv2.rectangle(img_out, (coord[0], coord[1]), (coord[0] + coord[2], coord[1] + coord[3]), (0, 0, 255), 1)
        if coord[4] is -1:
            cv2.putText(img_out, 'B_C', (coord[0], coord[1]), font, .5, (0, 0, 255), 2)
            cv2.rectangle(img_out, (coord[0], coord[1]), (coord[0] + coord[2], coord[1] + coord[3]), (0, 0, 255), 1)
        if coord[4] is 0:
            cv2.putText(img_out, 'F_NH', (coord[0], coord[1]), font, .5, (255, 0, 255), 2)
            cv2.rectangle(img_out, (coord[0], coord[1]), (coord[0] + coord[2], coord[1] + coord[3]), (0, 0, 255), 1)
        if coord[4] is 1:
            cv2.putText(img_out, 'H_NH', (coord[0], coord[1]), font, .5, (255, 0, 255), 2)
            cv2.rectangle(img_out, (coord[0], coord[1]), (coord[0] + coord[2], coord[1] + coord[3]), (0, 0, 255), 1)
        if coord[4] is 2:
            cv2.putText(img_out, 'W_NH', (coord[0], coord[1]), font, .5, (255, 0, 255), 2)
            cv2.rectangle(img_out, (coord[0], coord[1]), (coord[0] + coord[2], coord[1] + coord[3]), (0, 0, 255), 1)
        if coord[4] is 3:
            cv2.putText(img_out, 'S', (coord[0], coord[1]), font, .5, (0, 255, 255), 2)
            cv2.rectangle(img_out, (coord[0], coord[1]), (coord[0] + coord[2], coord[1] + coord[3]), (0, 0, 255), 1)
        if coord[4] is 4:
            cv2.putText(img_out, 'F', (coord[0], coord[1]), font, .5, (0, 255, 255), 2)
            cv2.rectangle(img_out, (coord[0], coord[1]), (coord[0] + coord[2], coord[1] + coord[3]), (0, 0, 255), 1)
        if coord[4] is 5:
            cv2.putText(img_out, 'N', (coord[0], coord[1]), font, .5, (0, 255, 255), 2)
            cv2.rectangle(img_out, (coord[0], coord[1]), (coord[0] + coord[2], coord[1] + coord[3]), (0, 0, 255), 1)
        if coord[4] is 6:
            cv2.putText(img_out, 'W_R', (coord[0], coord[1]), font, .5, (255, 0, 0), 2)
            cv2.rectangle(img_out, (coord[0], coord[1]), (coord[0] + coord[2], coord[1] + coord[3]), (0, 0, 255), 1)
        if coord[4] is 7:
            cv2.putText(img_out, 'H_R', (coord[0], coord[1]), font, .5, (255, 0, 0), 2)
            cv2.rectangle(img_out, (coord[0], coord[1]), (coord[0] + coord[2], coord[1] + coord[3]), (0, 0, 255), 1)
        if coord[4] is 8:
            cv2.putText(img_out, 'Q_R', (coord[0], coord[1]), font, .5, (255, 0, 0), 2)
            cv2.rectangle(img_out, (coord[0], coord[1]), (coord[0] + coord[2], coord[1] + coord[3]), (0, 0, 255), 1)
        if coord[4] is 9:
            cv2.putText(img_out, 'E_R', (coord[0], coord[1]), font, .5, (255, 0, 0), 2)
            cv2.rectangle(img_out, (coord[0], coord[1]), (coord[0] + coord[2], coord[1] + coord[3]), (0, 0, 255), 1)
        if coord[4] is 10:
            cv2.putText(img_out, 'S_R', (coord[0], coord[1]), font, .5, (255, 0, 0), 2)
            cv2.rectangle(img_out, (coord[0], coord[1]), (coord[0] + coord[2], coord[1] + coord[3]), (0, 0, 255), 1)
        if coord[4] is 11:
            cv2.putText(img_out, 'Dot', (coord[0], coord[1]), font, .5, (0, 255, 0), 2)
            cv2.rectangle(img_out, (coord[0], coord[1]), (coord[0] + coord[2], coord[1] + coord[3]), (0, 0, 255), 1)
        if coord[4] is 12:
            cv2.putText(img_out, 'R', (coord[0], coord[1]), font, .5, (0, 255, 0), 2)
            cv2.rectangle(img_out, (coord[0], coord[1]), (coord[0] + coord[2], coord[1] + coord[3]), (0, 0, 255), 1)
        if coord[4] is 13:
            cv2.putText(img_out, 'R_E', (coord[0], coord[1]), font, .5, (0, 255, 0), 2)
            cv2.rectangle(img_out, (coord[0], coord[1]), (coord[0] + coord[2], coord[1] + coord[3]), (0, 0, 255), 1)

    cv2.imshow('img_out', img_out)
    cv2.waitKey(0)

cv2.destroyAllWindows()
cv2.imwrite(sheetname + 'v2.png', img_out)
