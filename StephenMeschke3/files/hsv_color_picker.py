import cv2
import numpy as np

# Capture the webcam (or enter path to video)
cap = cv2.VideoCapture('/home/alex/tfg_jugglingTrackingSiteswap/dataset/instagram/ss95_simeonjuggler.mp4')
#ss3_ayalooloooooo h,s,v,h1,s1,v1 127, 73, 39, 177, 191, 148 X
#ss3_juggleforyou h,s,v,h1,s1,v1 0, 9, 217, 22 ,46, 255
#ss423_benjamin_klopcic h,s,v,h1,s1,v1 2, 16, 204, 25, 42, 255
#ss441_maxavener h,s,v,h1,s1,v1 21, 166, 157, 27, 255, 236
#ss531_yaron531 h,s,v,h1,s1,v1 159, 150, 113, 175, 255, 255
#ss5551_maxavener h,s,v,h1,s1,v1 23, 32, 158, 40, 255, 229
#ss534_benjamin_klopcic h,s,v,h1,s1,v1 7, 23, 221, 29, 65, 236
#ss5_chrizes3 h,s,v,h1,s1,v1 14, 45, 204, 29, 69, 255
#ss5_jugglingaroundtheworld h,s,v,h1,s1,v1 165, 126, 98, 178, 244, 155
#ss5_rohanjuggler h,s,v,h1,s1,v1 23, 95, 101, 30, 255, 255
#ss645_rohanjuggler h,s,v,h1,s1,v1 23, 95, 101, 30, 255, 255
#ss69163_thejugglingalex h,s,v,h1,s1,v1 0, 130, 179, 9, 217, 237 Igual quitar luz de navidad
#ss97531_rohanjuggler h,s,v,h1,s1,v1 26, 148, 97, 35, 244, 229 Igual quitar bolas del suelo
#ss6_cinqcent34 h,s,v,h1,s1,v1 172, 59, 219, 183, 184, 253
#ss7_gonzalopurvis h,s,v,h1,s1,v1 13, 43, 162, 35, 196, 255 recortar estanteria izquierda
#ss7_herrakoskinen h,s,v,h1,s1,v1 169, 160, 100, 179, 255, 186
#ss7_rohanjuggler h,s,v,h1,s1,v1 17, 116, 128, 34, 211, 224
#ss7_simeonjuggler h,s,v,h1,s1,v1 90, 23, 94, 109, 152, 161
#ss95_simeonjuggler h,s,v,h1,s1,v1 90, 23, 94, 109, 152, 161
#ss95_rohanjuggler h,s,v,h1,s1,v1 20, 101, 117, 43, 237, 255
#ss8_spencethejuggler h,s,v,h1,s1,v1 9, 19, 197, 27, 68, 243 recortar marco
#ss97_spencethejuggler h,s,v,h1,s1,v1 7, 19, 230, 27, 43, 255 Igual quitar calcetines
#ss9_rohanjuggler h,s,v,h1,s1,v1 95, 85, 48, 117, 255, 190


def nothing(arg): pass

#takes an image, and a lower and upper bound
#returns only the parts of the image in bounds
def only_color(frame, color_ranges, morph):
    h,s,v,h1,s1,v1 = color_ranges
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # define range of blue color in HSV
    lower = np.array([h,s,v])
    upper = np.array([h1,s1,v1])
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower, upper)
    #define kernel size (for touching up the image)
    #kernel = np.ones((morph, morph),np.uint8)
    #touch up
    #mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)
    return res, mask

#setup trackbars
cv2.namedWindow('image')
cv2.createTrackbar('h', 'image', 0,255, nothing)
cv2.createTrackbar('s', 'image', 0,255, nothing)
cv2.createTrackbar('v', 'image', 0,255, nothing)
cv2.createTrackbar('h1', 'image', 255,255, nothing)
cv2.createTrackbar('s1', 'image', 255,255, nothing)
cv2.createTrackbar('v1', 'image', 255,255, nothing)
cv2.createTrackbar('morph', 'image', 0,10, nothing)

#main loop of the program
number_of_frame = 0
if number_of_frame == 0:
    number_of_frame = cap.get(cv2.CAP_PROP_FRAME_COUNT)
for i in range(int(number_of_frame//2)):
    _, img = cap.read()
while True:

    #read image from the video

    #get trackbar values
    h= cv2.getTrackbarPos('h', 'image')
    s= cv2.getTrackbarPos('s', 'image')
    v= cv2.getTrackbarPos('v', 'image')
    h1= cv2.getTrackbarPos('h1', 'image')
    s1= cv2.getTrackbarPos('s1', 'image')
    v1= cv2.getTrackbarPos('v1', 'image')
    morph = cv2.getTrackbarPos('morph', 'image')
    
    #extract only the colors between h,s,v and h1,s1,v1
    imS = cv2.resize(img, (960, 540)) 
    img2, mask = only_color(imS, (h,s,v,h1,s1,v1), morph)
    
    #show the image and wait
    cv2.imshow('img', imS)
    cv2.imshow('image', mask)
    k=cv2.waitKey(1)
    if k==27: break

#print calues
print('h,s,v,h1,s1,v1 -> {},{},{},{},{},{}'.format(h,s,v,h1,s1,v1))

#release the video to avoid memory leaks, and close the window
cap.release()
cv2.destroyAllWindows()
