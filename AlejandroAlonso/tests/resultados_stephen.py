import cv2
import numpy as np
from matplotlib import pyplot as plt


def contour_center(c):
    M = cv2.moments(c)
    try: center = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
    except: center = 0,0
    return center

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
                    if overlap > threshold_value:
                        overlaps.add(j)
        
    contours = [x for i, x in enumerate(contours) if i not in overlaps]

    return contours

img = cv2.imread('../../dataset/tests/frame.png')

RGBimage = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

h,s,v,h1,s1,v1 = 35,30,150,185,120,255


hsv = cv2.cvtColor(RGBimage, cv2.COLOR_BGR2HSV)
# define range of blue color in HSV
lower = np.array([h,s,v])
upper = np.array([h1,s1,v1])
# Threshold the HSV image to get only blue colors
mask = cv2.inRange(hsv, lower, upper)
# Bitwise-AND mask and original image
res = cv2.bitwise_and(RGBimage,RGBimage, mask= mask)


imgray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
_ ,thresh = cv2.threshold(imgray,0,255,0)
contours, _ = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

square_len=50
img_copy = img.copy()
for c in contours:
    coords_x,coords_y = contour_center(c)
    start_point = (coords_x-square_len//2, coords_y-square_len//2)
    end_point = (coords_x+square_len//2, coords_y+square_len//2)
    cv2.rectangle(img_copy, start_point, end_point, (0, 0, 255), 2)

non_max_suppresion_threshold=50
img_copy2 = img.copy()
contours2 = contours_non_max_suppression(contours,non_max_suppresion_threshold)
for c in contours2:
    coords_x,coords_y = contour_center(c)
    start_point = (coords_x-square_len//2, coords_y-square_len//2)
    end_point = (coords_x+square_len//2, coords_y+square_len//2)
    cv2.rectangle(img_copy2, start_point, end_point, (0, 0, 255), 2)

fig, ax = plt.subplots(nrows=2, ncols=3)
fig.tight_layout()

ax[0][0].imshow(RGBimage)
ax[0][0].set_title("Frame inicial")

ax[0][1].imshow(hsv)
ax[0][1].set_title("Frame hsv")

ax[0][2].imshow(mask, cmap='gray')
ax[0][2].set_title("Máscara del only_color")

ax[1][0].imshow(res)
ax[1][0].set_title("Resultado only_color")

ax[1][1].imshow(imgray, cmap='gray')
ax[1][1].set_title("Resultado only_color gris")

ax[1][2].imshow(thresh, cmap='gray')
ax[1][2].set_title("Resultado only_color tras threshold,\n antes de sacar contornos")

fig, ax = plt.subplots(nrows=1, ncols=2)
fig.tight_layout()
ax[0].imshow(img_copy)
ax[0].set_title("Resultado contornos")

ax[1].imshow(img_copy2)
ax[1].set_title("Resultado contornos supresion overlaps")


plt.show()