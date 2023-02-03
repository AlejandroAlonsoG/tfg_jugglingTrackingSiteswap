import numpy as np
import cv2

cap = cv2.VideoCapture('/home/alex/tfg_jugglingTrackingSiteswap/dataset/ss3_red_AlejandroAlonso.mp4')

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

# initializing subtractor
fgbg = cv2.bgsegm.createBackgroundSubtractorGMG()

object_detector = cv2.createBackgroundSubtractorMOG2(
                        history=100,
                        varThreshold=10)

cv2.namedWindow('img', cv2.WINDOW_NORMAL)
cv2.namedWindow('img2', cv2.WINDOW_NORMAL)

while(1):
	ret, frame = cap.read()

	# applying on each frame
	fgmask = fgbg.apply(frame)
	fgmask2 = object_detector.apply(frame)

	fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)	

	cv2.imshow('img', fgmask)
	k = cv2.waitKey(1)
	if k == 27:
		break

	cv2.imshow('img2', fgmask2)


cap.release()
cv2.destroyAllWindows()
