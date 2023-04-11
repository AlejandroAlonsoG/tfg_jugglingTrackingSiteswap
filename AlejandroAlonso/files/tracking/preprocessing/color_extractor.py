import cv2
import numpy as np
import colorsys

def get_center( contour ):
    M = cv2.moments(contour)
    return [ int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]) ]


# Pilla el color más detectado y hace un rango desde ahi
def color_extractor(source_path, min_contour_area=1000, h_range=2, sv_range1=75, sv_range2=175, size=5):
    cap = cv2.VideoCapture(source_path)

    # Object detection from stable camera
    object_detector = cv2.createBackgroundSubtractorMOG2(
                        history=100,
                        varThreshold=40)

    ret, frame = cap.read()
    color_dict = {}
    current_frame = 0
    while ret:
        mask = object_detector.apply(frame) # Básicamente la máscara es aplicar BackgroundSubstractor con 100 y 40 a toda la imagen
        _, mask = cv2.threshold( mask, 254, 255, # Se pasa la máscara por un threshold de grises
                                    cv2.THRESH_BINARY )
        contours, _ = cv2.findContours( mask, # Desde el resultado de esa máscara se sacan los contornos
                                        cv2.RETR_TREE,
                                        cv2.CHAIN_APPROX_SIMPLE )

        image = frame

        for c in contours:
            area = cv2.contourArea(c)
            if area > min_contour_area:
                # Approx es un polígono aproximado desde el contorno, a mayor cte (0.05 en este caso) es más estricto
                approx = cv2.approxPolyDP(c,0.05*cv2.arcLength(c,True),True)
                # La longitud es el número de lados, pedimos que mínimo sea tipo cuadrado
                if len(approx) > 4:
                    # Comprueba si es convexo, para que sea mas tipo cuadrado, porque las manos muchas veces pilla cuatro lados pero dos hacia dentro o similar
                    if cv2.isContourConvex(approx):
                        center = get_center(c)
                        cx, cy = center
                        # Pilla los colores de los píxeles en la region que sea
                        print(current_frame)
                        for i in range(-size//2,size//2 + 1):
                            for j in range(-size//2,size//2 + 1):
                                (b,g,r) = image[cy+i, cx+j]
                                if (b,g,r) in color_dict:
                                    color_dict[(b,g,r)] += 1
                                else:
                                    color_dict[(b,g,r)] = 1
                

        ret, frame = cap.read()
        current_frame += 1
        print(current_frame)

    # Pilla el color más repetido y lo pasa a hsv
    (b,g,r) = max(color_dict, key=color_dict.get)
    (h, s, v) = colorsys.rgb_to_hsv(r,g,b)
    # hsv de colorsys es sobre 1,1,255 en vez de 180, 255, 255 
    (h,s,v) = (int(180*h), int(255*s), v)

    cap.release()
    s1 = min(s, sv_range1)
    s2 = max(s, sv_range2)
    v1 = min(v, sv_range1)
    v2 = max(v, sv_range2) 
    # h selecciona el color, se da un poco de flexibilidad, s y v seleccionan tonos/sombras de ese color, se cogen todas (se podría hacer un rango mas pequeño)
    return h-h_range, s1, v1, h+h_range, s2, v2


# Hace un histograma con los canales h, s y v y desde ahí pilla los picos y las zonas cercanas segun el umbral. No funciona bien
def color_extractor_test(source_path, min_contour_area=1000, index_umbral=0.6, size=5):
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
                for i in range(-size//2,size//2 + 1):
                    for j in range(-size//2,size//2 + 1):
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

    return res["h"][0], res["s"][0], int(res["v"][0]), res["h"][1], res["s"][1], int(res["v"][1])

# Pilla el color más detectado y hace un rango desde ahi
def color_extractor_test2(source_path, min_contour_area=1000, h_range=2, sv_range1=75, sv_range2=175, size=5):
    cap = cv2.VideoCapture(source_path)

    # Object detection from stable camera
    object_detector = cv2.createBackgroundSubtractorMOG2(
                        history=100,
                        varThreshold=40)

    ret, frame = cap.read()
    color_dict = {}
    current_frame = 0
    total_b = 0
    total_g = 0
    total_r = 0
    while ret:
        mask = object_detector.apply(frame) # Básicamente la máscara es aplicar BackgroundSubstractor con 100 y 40 a toda la imagen
        _, mask = cv2.threshold( mask, 254, 255, # Se pasa la máscara por un threshold de grises
                                    cv2.THRESH_BINARY )
        contours, _ = cv2.findContours( mask, # Desde el resultado de esa máscara se sacan los contornos
                                        cv2.RETR_TREE,
                                        cv2.CHAIN_APPROX_SIMPLE )

        image = frame

        for c in contours:
            area = cv2.contourArea(c)
            if area > min_contour_area:
                # Approx es un polígono aproximado desde el contorno, a mayor cte (0.05 en este caso) es más estricto
                approx = cv2.approxPolyDP(c,0.05*cv2.arcLength(c,True),True)
                # La longitud es el número de lados, pedimos que mínimo sea tipo cuadrado
                if len(approx) > 4:
                    # Comprueba si es convexo, para que sea mas tipo cuadrado, porque las manos muchas veces pilla cuatro lados pero dos hacia dentro o similar
                    if cv2.isContourConvex(approx):
                        center = get_center(c)
                        cx, cy = center
                        # Pilla los colores de los píxeles en la region que sea
                        print(current_frame)
                        for i in range(-size//2,size//2 + 1):
                            for j in range(-size//2,size//2 + 1):
                                (b,g,r) = image[cy+i, cx+j]
                                total_b += b
                                total_g += g
                                total_r += r
                

        ret, frame = cap.read()
        current_frame += 1
        print(current_frame)

    # Pilla el color más repetido y lo pasa a hsv
    (b,g,r) = total_b//(current_frame*25), total_g//(current_frame*25), total_r//(current_frame*25)
    (h, s, v) = colorsys.rgb_to_hsv(r,g,b)
    # hsv de colorsys es sobre 1,1,255 en vez de 180, 255, 255 
    (h,s,v) = (int(180*h), int(255*s), v)

    cap.release()
    s1 = min(s, sv_range1)
    s2 = max(s, sv_range2)
    v1 = min(v, sv_range1)
    v2 = max(v, sv_range2) 
    # h selecciona el color, se da un poco de flexibilidad, s y v seleccionan tonos/sombras de ese color, se cogen todas (se podría hacer un rango mas pequeño)
    return h-h_range, s1, v1, h+h_range, s2, v2