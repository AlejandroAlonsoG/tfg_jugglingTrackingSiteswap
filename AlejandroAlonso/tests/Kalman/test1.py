import numpy as np
import cv2, sys
from kalman_filter import KalmanFilter


#cv2.namedWindow('img', cv2.WINDOW_NORMAL)


coords = [(518,1229),(515,1252),(516,1247),(516,1250),(516,1253),(518,1252),(521,1249),(528,1237),(534,1216),(538,1185),(542,1154),(544,1078),(550,1011),(558,965),(564,932),(569,899),(571,864),(573,829),(580,804),(590,791),(599,780),(608,779),(618,785),(628,792),(635,803),(639,823),(644,849),(654,876),(665,904),(676,936),(686,974),(693,1008),(701,1037),(707,1057),(708,1073),(712,1093),(709,1116),(694,1136),(681,1155),(671,1172),(664,1190),(659,1206),(655,1215),(647,1217),(644,1223),(635,1222),(621,1197),(606,1162),(598,1136),(588,1095),(583,1042),(578,989),(573,939),(569,902),(565,882),(560,862),(554,838),(548,814),(546,797),(542,788),(536,793),(530,802),(527,816),(524,835),(522,858),(519,885)]

dt = float(sys.argv[1])
u_x = float(sys.argv[2])
u_y = float(sys.argv[3])
std_acc = float(sys.argv[4])
x_std_meas = float(sys.argv[5])
y_std_meas = float(sys.argv[6])

#KF = KalmanFilter(0.1, 1, 1, 1, 0.1,0.1)
KF = KalmanFilter(dt, u_x,u_y, std_acc, x_std_meas, y_std_meas)

err_x = 0
err_y = 0
for coord in coords:
    """ height, width = 1920, 1080
    img = np.zeros((height, width, 3), np.uint8)
    img[:, :] = [255, 255, 255]


    cv2.circle(img, coord, 10, (0, 191, 255), 2) """

    (x,y) = KF.predict()
    #cv2.rectangle(img, (int(x - 15), int(y - 15)), (int(x + 15), int(y + 15)), (255, 0, 0), 2)

    (x1, y1) = KF.update(np.array([[coord[0]], [coord[1]]]))
    """ cv2.rectangle(img, (int(x1 - 15), int(y1 - 15)), (int(x1 + 15), int(y1 + 15)), (0, 0, 255), 2)

    cv2.putText(img, "Estimated Position", (int(x1 + 15), int(y1 + 10)), 0, 0.5, (0, 0, 255), 2)
    cv2.putText(img, "Predicted Position", (int(x + 15), int(y)), 0, 0.5, (255, 0, 0), 2)
    cv2.putText(img, "Measured Position", (int(coord[0] + 15), int(coord[1] - 15)), 0, 0.5, (0,191,255), 2)


    cv2.imshow('img', img)
    cv2.waitKey(1) """
    #print(x,y)
    err_x += abs(coord[0]-float(x))
    err_y += abs(coord[1]-float(y))

print(err_x/len(coords),err_y/len(coords))

""" cv2.imshow('img', img)
cv2.waitKey(0)

cv2.destroyAllWindows() """