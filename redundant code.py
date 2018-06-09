#get location of treble_clef
res_treble = cv2.matchTemplate(img_gray, treble, cv2.TM_CCOEFF_NORMED)
threshold_treble = 0.60
loc_treble = np.where( res_treble >= threshold_treble)
if loc_treble is not None:
    for pt in sorted(zip(*loc_treble[::-1]), key = lambda x:x[0]):
        #for each pt determine center, compare to within range of other centers
        #get (X,Y)
        nX = pt[0]
        nY = pt[1]
        ##if first entry
        if first is True:
            X.append(nX)
            Y.append(nY)
            type.append(5)
            cv2.rectangle(img_sheet_music, pt, (nX + tw, nY + th), (255, 0, 0), 2)
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
                type.append(5)
                #if in range, ignore, else draw
                cv2.rectangle(img_sheet_music, pt, (nX + tw, nY + th), (255, 0, 0), 1)

#get location of base_clef
res_base = cv2.matchTemplate(img_gray, base, cv2.TM_CCOEFF_NORMED)
threshold_base = 0.60
loc_base = np.where( res_base >= threshold_base)
if loc_base is not None:
    for pt in sorted(zip(*loc_base[::-1]), key = lambda x:x[0]):
        #for each pt determine center, compare to within range of other centers
        #get (X,Y)
        nX = pt[0]
        nY = pt[1]
        #print(pt)
        ##if first entry
        if first is True:
            X.append(nX)
            Y.append(nY)
            type.append(6)
            cv2.rectangle(img_sheet_music, pt, (nX + bw, nY + bh), (255, 0, 0), 2)
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
                type.append(6)
                #if in range, ignore, else draw
                cv2.rectangle(img_sheet_music, pt, (nX + bw, nY + bh), (255, 0, 0), 1)

#get location of note_heads
res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
threshold = 0.73
loc = np.where( res >= threshold)
if loc is not None:
for pt in sorted(zip(*loc[::-1]), key = lambda x:x[0]):
    #for each pt determine center, compare to within range of other centers
    #get (X,Y)
    nX = pt[0]
    nY = pt[1]
    #print(pt)
    if nX > left and nY < top:
        #if first entry
        if first is True:
            X.append(nX)
            Y.append(nY)
            type.append(0)
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
                type.append(0)
                #if in range, ignore, else draw
                cv2.rectangle(img_sheet_music, pt, (nX + w, nY + h), (0, 0, 255), 1)

#get location of hollow_note_heads
threshold2 = 0.62
res2 = cv2.matchTemplate(img_gray, template2, cv2.TM_CCOEFF_NORMED)
loc2 = np.where( res2 >= threshold2)
if loc2 is not None:
    for pt in sorted(zip(*loc2[::-1]), key = lambda x:x[0]):
        #for each pt determine center, compare to within range of other centers
        #get (X,Y)
        nX = pt[0]
        nY = pt[1]
        #print(pt)
        if nX > left and nY < top:
            #if first entry
            if first is True:
                X.append(nX)
                Y.append(nY)
                type.append(1)
                cv2.rectangle(img_sheet_music, pt, (nX + w2, nY + h2), (0, 0, 255), 2)
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
                    type.append(1)
                    #if in range, ignore, else draw
                    cv2.rectangle(img_sheet_music, pt, (nX + w2, nY + h2), (0, 0, 255), 1)

#get location of sharps
threshold3 = 0.62
res3 = cv2.matchTemplate(img_gray, template3, cv2.TM_CCOEFF_NORMED)
loc3 = np.where( res3 >= threshold3)
if loc3 is not None:
    for pt in sorted(zip(*loc3[::-1]), key = lambda x:x[0]):
        #for each pt determine center, compare to within range of other centers
        #get (X,Y)
        nX = pt[0]
        nY = pt[1]
        #print(pt)
        if nX > left and nY < top:
            #if first entry
            if first is True:
                X.append(nX)
                Y.append(nY)
                type.append(2)
                cv2.rectangle(img_sheet_music, pt, (nX + w2, nY + h2), (255, 0, 0), 2)
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
                    type.append(2)
                    #if in range, ignore, else draw
                    cv2.rectangle(img_sheet_music, pt, (nX + w3, nY + h3), (255, 0, 0), 1)

#get location of flats
threshold4 = 0.70
res4 = cv2.matchTemplate(img_gray, template4, cv2.TM_CCOEFF_NORMED)
loc4 = np.where( res4 >= threshold4)
if loc4 is not None:
    for pt in sorted(zip(*loc4[::-1]), key = lambda x:x[0]):
        #for each pt determine center, compare to within range of other centers
        #get (X,Y)
        nX = pt[0]
        nY = pt[1]
        #print(pt)
        if nX > left and nY < top:
            #if first entry
            if first is True:
                X.append(nX)
                Y.append(nY)
                type.append(3)
                cv2.rectangle(img_sheet_music, pt, (nX + w4, nY + h4), (255, 0, 0), 2)
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
                    type.append(3)
                    #if in range, ignore, else draw
                    cv2.rectangle(img_sheet_music, pt, (nX + w4, nY + h4), (255, 0, 0), 1)

#get location of naturals
threshold5 = 0.70
res5 = cv2.matchTemplate(img_gray, template5, cv2.TM_CCOEFF_NORMED)
loc5 = np.where( res5 >= threshold5)
if loc5 is not None:
    for pt in sorted(zip(*loc5[::-1]), key = lambda x:x[0]):
        #for each pt determine center, compare to within range of other centers
        #get (X,Y)
        nX = pt[0]
        nY = pt[1]
        #print(pt)
        if nX > left and nY < top:
            #if first entry
            if first is True:
                X.append(nX)
                Y.append(nY)
                type.append(4)
                cv2.rectangle(img_sheet_music, pt, (nX + w5, nY + h5), (255, 0, 0), 2)
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
                    type.append(4)
                    #if in range, ignore, else draw
                    cv2.rectangle(img_sheet_music, pt, (nX + w5, nY + h5), (255, 0, 0), 1)


#remove lines in lines list from grayscale image, dilate to remove holes
for yCoord in lines:
    cv2.rectangle(img_gray, (0, yCoord), (1700, yCoord+3), (255, 255, 255), -1)
kernel = np.ones((5,5), np.uint8)
img_gray = cv2.erode(img_gray, kernel, iterations=1)
img_gray = cv2.dilate(img_gray, kernel, iterations=1)
cv2.imshow("res", img_gray)
cv2.waitKey(0)
