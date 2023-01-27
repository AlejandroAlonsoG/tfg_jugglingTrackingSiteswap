import numpy as np
import cv2

import colorsys 
 
def HSVToRGB(h, s, v): 
 (r, g, b) = colorsys.hsv_to_rgb(h, s, v) 
 return (int(255*r), int(255*g), int(255*b)) 
 
def getDistinctColors(id, num_balls):
    h = (int(360/num_balls * id))
    r, g, b = cv2.cvtColor(np.uint8([[[h / 2, 255, 255]]]), cv2.COLOR_HSV2BGR)[0][0]
    return (int(r), int(g), int(b))

def get_color(id, num_balls):
    # 255*3 porque hace todas las combinaciones en rgb, /numballs y * id para coger los valores más separados entre ids
    value = (255*3)/(num_balls-1) * id
    # Devuelve el código rgb correspondiente a ese color

    if value%255 == 0 and value != 0:
        take = 255
    else:
        take = 0

    if value > 255*2:
        return (255, 255, int(value%255) + take)
    elif value > 255:
        return (255, int(value%255) + take, 0)
    else:
        return (int(value%255) + take, 0, 0)

colors = []
for i in range(0, 5):
    colors.append(getDistinctColors(i, 5))

print(colors)

cv2.namedWindow('img', cv2.WINDOW_NORMAL)
height, width = 1920, 1080
img = np.zeros((height, width, 3), np.uint8)
img[:, :] = [255, 255, 255]

for i in range (0,5):
    #cv2.circle(img, (int(1920/2),int((1080/5)*i)), 10, colors[i], 2)
    x,y = (540,int((1920/5)*i)+int(1920/10))
    cv2.circle(img, (x,y), 50, colors[i], -1)
    cv2.putText(img, str(colors[i]), (x+50, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)

cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()