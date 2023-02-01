import cv2
import numpy as np

def get_center( contour ):
    M = cv2.moments(contour)
    return [ int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]) ]

def color_extractor(source_path, min_contour_area=1000, index_umbral=0.7):
    cap = cv2.VideoCapture(source_path)

    # Object detection from stable camera
    object_detector = cv2.createBackgroundSubtractorMOG2(
                        history=100,
                        varThreshold=40)

    ret, frame = cap.read()
    color_dict = {}
    color_dict["h"] = []
    color_dict["s"] = []
    color_dict["v"] = []
    current_frame = 0
    while ret:
        mask = object_detector.apply(frame) # Básicamente la máscara es aplicar BackgroundSubstractor con 100 y 40 a toda la imagen
        _, mask = cv2.threshold( mask, 254, 255, # Se pasa la máscara por un threshold de grises
                                    cv2.THRESH_BINARY )
        contours, _ = cv2.findContours( mask, # Desde el resultado de esa máscara se sacan los contornos
                                        cv2.RETR_TREE,
                                        cv2.CHAIN_APPROX_SIMPLE )

        image = frame
        hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # ELIMINAR CONTORNOS PRÓXIMOS PARA QUITARSE LAS MANOS DE ENCIMA LA MAYORÍA DEL TIEMPO
        for c in contours:
            # print(f"to: {to}")
            area = cv2.contourArea(c)
            if area > min_contour_area:
                #cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
                center = get_center(c)
                cx, cy = center
                # COGER COLOR EN 5x5 pej
                for i in range(-2,3):
                    for j in range(-2,3):
                        color = hsv_img[cy+i, cx+j]
                #cv2.circle(image, (cx, cy), 20, (0, 255, 0), -1)
                color_dict["h"].append(color[0])
                color_dict["s"].append(color[1])
                color_dict["v"].append(color[2])

        ret, frame = cap.read()
        current_frame += 1

    canals = ["h", "s", "v"]
    res = {}
    for canal in canals:
        histogram, _ = np.histogram(
            color_dict[canal], bins=256, range=(0, 256)
        )
        peaks = np.where(histogram > index_umbral*histogram.max())[0]
        min_idx, max_idx = peaks[0], peaks[-1]
        res[canal] = (min_idx, max_idx)

    cap.release()

    return res["h"][0], res["s"][0], res["v"][0], res["h"][1], res["s"][1], res["v"][1]