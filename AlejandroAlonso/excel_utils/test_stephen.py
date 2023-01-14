# Import libraries
import cv2, numpy as np

import excel_utils as eu
system = "StephenMeschke"
ss = "ss5"

# H,S,V range of the object to be tracked

#h,s,v,h1,s1,v1 = 150,77,70,255,255,255 #RED
h,s,v,h1,s1,v1 = 35,30,150,185,120,255 #RED_Alex

# Find these values using hsv_color_picker.py
#h,s,v,h1,s1,v1 = 156,74,76,166,255,255 #pink
#h,s,v,h1,s1,v1 = 27,0,0,82,190,255 #GREEN

# Define the source path
#cap = cv2.VideoCapture('/home/alex/tfg_jugglingTrackingSiteswap/dataset/tests/short.mp4')
cap = cv2.VideoCapture('/home/alex/tfg_jugglingTrackingSiteswap/dataset/ss5_red_AlejandroAlonso.mp4')

non_max_suppresion_threshold=50

# Takes image and color, returns parts of image that are that color
def only_color(frame, hsv_range):
    (b,r,g,b1,r1,g1) = hsv_range
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # define range of blue color in HSV
    lower = np.array([b,r,g])
    upper = np.array([b1,r1,g1])
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower, upper)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)
    return res, mask

#finds the largest contour in a list of contours
#returns a single contour
def largest_contour(contours):
    c = max(contours, key=cv2.contourArea)
    return c[0]

#takes an image and the threshold value returns the contours
def get_contours(im, threshold_value):
    imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    _ ,thresh = cv2.threshold(imgray,0,255,0)
    contours, _ = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    return contours

def contours_non_max_suppression(contours, threshold_value, use_distance=True):
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    overlaps = set()

    # Usa el threshold como una distancia, entonces elimina las regiones mas pequeñas que esten demasiado cerca
    if use_distance:
        for i in range(len(contours)):
            for j in range(i+1, len(contours)):
                point1 = contour_center(contours[i])
                point2 = contour_center(contours[j])
                dist = np.linalg.norm(np.array(point1) - np.array(point2))
                if dist < threshold_value:
                    overlaps.add(j)
    # Usa el threshold para comprobar la interseccion, de forma que elimina regiones superpuestas en demasiada medida
    else:
        for i in range(len(contours)):
            for j in range(i+1, len(contours)):
                # Saco rectangulos que definen cada contorno
                (x1,y1,w1,h1) = cv2.boundingRect(contours[i])
                (x2,y2,w2,h2) = cv2.boundingRect(contours[j])
                a = (x1, y1)
                b = (x1+w1, y1+h1)
                c = (x2, y2)
                d = (x2+w2, y2+h2)
                width = min(b[0], d[0]) - max(a[0], c[0])
                height = min(b[1], d[1]) - max(a[1], c[1])
                # Si hay alguna interseccion
                if min(width,height) > 0:
                    intersection = width*height
                    area1 = (b[0]-a[0])*(b[1]-a[1])
                    area2 = (d[0]-c[0])*(d[1]-c[1])
                    union = area1 + area2 - intersection
                    # Si la interseccion es suficientemente grande la marco como overlap
                    overlap=intersection/union
                    print(overlap)
                    if overlap > threshold_value:
                        overlaps.add(j)
        
    contours = [x for i, x in enumerate(contours) if i not in overlaps]

    return contours

def order_contours(contours, prev_contours):
    ordered_contours = []
    dist_matrix = np.zeros((len(contours),len(prev_contours)))

    for idx,(prev_c,tag) in enumerate(prev_contours):
        for jdx, curr_c in enumerate(contours):
            prev_center = contour_center(prev_c)
            curr_center = contour_center(curr_c)
            curr_dist = np.linalg.norm(np.array(prev_center) - np.array(curr_center))
            dist_matrix[jdx,idx] = curr_dist
    
    max_dist = dist_matrix.max()
    used_tags = []
    for i in range(min(dist_matrix.shape)):
        min_value_index = np.unravel_index(dist_matrix.argmin(), dist_matrix.shape)
        ordered_contours.insert(min_value_index[1], (contours[min_value_index[0]], min_value_index[1]))
        used_tags.append(min_value_index[1])
        dist_matrix[min_value_index[0],:] = max_dist+1
        dist_matrix[:,min_value_index[1]] = max_dist+1

    if(len(prev_contours)<len(contours)):
        for i in range(len(contours)):
            if i not in used_tags:
                ordered_contours.insert(i, (contours[i], i))
    elif(len(contours)<len(prev_contours)):
        for i in range(len(prev_contours)):
            if i not in used_tags:
                ordered_contours.insert(i, (None, i))

    return ordered_contours



#finds the center of a contour
#takes a single contour
#returns (x,y) position of the contour
def contour_center(c):
    M = cv2.moments(c)
    try: center = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
    except: center = 0,0
    return center

# Create list to save data
frame_number, prev_contours = 0, []
contour_tag = 0

book = eu.book_initializer(system,ss) #*edit*
# Iterate though each frame of video
while True:
    
    # Read image from the video
    _, img = cap.read()
    

    # Chech if the video is over
    try: l = img.shape
    except: break

    img_copy = img.copy()
    
    # Segment the image by color
    img, mask = only_color(img, (h,s,v,h1,s1,v1))

    # Find the contours in the image
    contours = get_contours(img, 0)

    # If there are contours found in the image:
    if len(contours)>0:
        """ try:
            # Sort the contours by area
            c = max(contours, key=cv2.contourArea)
            # Draw the contours on the image
            img = cv2.drawContours(img_copy, c ,-1, (0,0,255), 14)
            # Add the data from the contour to the list
            positions.append(contour_center(c))
        except: pass """
        contours = contours_non_max_suppression(contours, non_max_suppresion_threshold)
        if len(prev_contours) == 0:
            tagged_contours = []
            for c in contours:
                tagged_contours.append((c,contour_tag))
                contour_tag+=1
            prev_contours = tagged_contours
        else:
            tagged_contours = order_contours(contours, prev_contours)
            prev_contours = tagged_contours
        for id, (c,tag) in enumerate(tagged_contours):
            if c is not None:
                # Draw the contours on the image
                img = cv2.drawContours(img_copy, c ,-1, (0,0,255), 14)
                # Add the data from the contour to the list
                center = contour_center(c)
                if center != (0,0):
                    eu.book_writer(book, frame_number+1, id, contour_center(c))
            else:
                eu.book_writer(book, frame_number+1, id, None)

    frame_number += 1
    #show the image and wait 1080x1920
    imS = cv2.resize(img_copy, (540, 960))
    cv2.imshow('img', imS)
    #cv2.imshow('img', cv2.resize(img, (480,700)))
    k=cv2.waitKey(1)
    if k==27: break
    
#release the video to avoid memory leaks, and close the window
cap.release()
cv2.destroyAllWindows()

print('finished tracking')
#write data
""" import csv
with open(output_path, 'w') as csvfile:
    fieldnames = ['x_position', 'y_position']
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writeheader()
    for position in positions:
        x, y = position[0], position[1]
        writer.writerow({'x_position': x, 'y_position': y}) """
        

eu.book_saver(book,system,ss, sanitize=False)  #*edit*

print('finished writing data')
