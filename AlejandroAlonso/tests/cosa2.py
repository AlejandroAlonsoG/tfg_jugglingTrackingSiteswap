import cv2
import numpy as np

img = cv2.imread('/home/alex/tfg_jugglingTrackingSiteswap/dataset/tests/frame.png') 

""" padding = np.zeros((img.shape[1]))
padding[:] = [255, 255, 255]

img[:,] + padding """

img = cv2.copyMakeBorder(img, 0, 0, 0, img.shape[1], cv2.BORDER_CONSTANT, None, value = 0)

cv2.namedWindow('img', cv2.WINDOW_NORMAL)
cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
