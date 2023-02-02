import cv2
import numpy as np
import colorsys

def get_center( contour ):
    M = cv2.moments(contour)
    return [ int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]) ]

# Hace un histograma con los canales h, s y v y desde ahí pilla los picos y las zonas cercanas segun el umbral
def color_extractor(source_path, min_contour_area=1000, index_umbral=10, size=5):
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

    return res["h"][0], res["s"][0], res["v"][0], res["h"][1], res["s"][1], res["v"][1]

# Pilla el color más detectado y hace un rango desde ahi
def color_extractor_2(source_path, min_contour_area=1000, index_umbral=0.7, size=5):
    cap = cv2.VideoCapture(source_path)

    # Object detection from stable camera
    object_detector = cv2.createBackgroundSubtractorMOG2(
                        history=100,
                        varThreshold=40)

    ret, frame = cap.read()
    color_dict = {}
    current_frame = 0
    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    while ret:
        mask = object_detector.apply(frame) # Básicamente la máscara es aplicar BackgroundSubstractor con 100 y 40 a toda la imagen
        _, mask = cv2.threshold( mask, 254, 255, # Se pasa la máscara por un threshold de grises
                                    cv2.THRESH_BINARY )
        contours, _ = cv2.findContours( mask, # Desde el resultado de esa máscara se sacan los contornos
                                        cv2.RETR_TREE,
                                        cv2.CHAIN_APPROX_SIMPLE )

        image = frame

        # ELIMINAR CONTORNOS PRÓXIMOS PARA QUITARSE LAS MANOS DE ENCIMA LA MAYORÍA DEL TIEMPO
        for c in contours:
            # print(f"to: {to}")
            area = cv2.contourArea(c)
            if area > min_contour_area:
                approx = cv2.approxPolyDP(c,0.05*cv2.arcLength(c,True),True)
                if len(approx) > 4:
                    k=cv2.isContourConvex(approx)
                    if k:
                        cv2.drawContours(image, [approx], -1, (0, 255, 0), 2)
                        center = get_center(c)
                        cx, cy = center
                        for i in range(-size//2,size//2 + 1):
                            for j in range(-size//2,size//2 + 1):
                                (b,g,r) = image[cy+i, cx+j]
                                if (b,g,r) in color_dict:
                                    color_dict[(b,g,r)] += 1
                                else:
                                    color_dict[(b,g,r)] = 1

                """ if cv2.isContourConvex(c):
                    cv2.drawContours(image, [c], -1, (0, 255, 0), 2) """
                cv2.imshow('img', image)
                #cv2.imshow('img', cv2.resize(img, (480,700)))
                k=cv2.waitKey(1)
                if k==27: break
                

        ret, frame = cap.read()
        current_frame += 1

    (b,g,r) = max(color_dict, key=color_dict.get)

    (h, s, v) = colorsys.rgb_to_hsv(r,g,b)

    cap.release()
    
    print(b,g,r, "->", color_dict[(b,g,r)])
    print(h,s,v, "->", 180*h,255*s,v)

    h = int(180*h)
    s = int(255*s)
    v = v

    cap = cv2.VideoCapture(source_path)
    ret, frame = cap.read()
    while ret:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        """ print(frame[cy, cx], "->", hsv[cy, cx])
        (b,g,r) = frame[cy, cx]
        (h, s, v) = colorsys.rgb_to_hsv(r,g,b)
        print(b,g,r, "->", int(180*h),int(255*s),int(v))
        print(hsv[cy, cx])   """      
        lower = np.array((h-2,0,0))
        upper = np.array((h+2,255,255))
        mask = cv2.inRange(hsv, lower, upper)

        res = cv2.bitwise_and(frame,frame, mask= mask)

        cv2.imshow('img', res)
        #cv2.imshow('img', cv2.resize(img, (480,700)))
        k=cv2.waitKey(0)
        if k==27: break

        ret, frame = cap.read()
        current_frame += 1


    cv2.destroyAllWindows()
    #return h-index_umbral, 100, 100, h+index_umbral, 255, 255
    return h, s, v, 0, 0, 0

source_path = '/home/alex/tfg_jugglingTrackingSiteswap/dataset/tests/short.mp4'
color_extractor_2(source_path, index_umbral=0.6, size=1)