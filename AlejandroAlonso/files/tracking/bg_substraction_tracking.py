import cv2
import numpy as np
import excel_utils_debugging as eu
import prediction.kalman_prediction_utils as kpu

def contour_center(c):
    M = cv2.moments(c)
    try: center = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
    except: center = 0,0
    return center


# Pilla el color más detectado y hace un rango desde ahi
def bg_substraction_tracking(source_path, min_contour_area=1000, enclosing_area_diff=0.5, visualize=False):
    system = "BgSubstractionTracking"
    ss=(source_path.split('/')[-1]).split('.')[0]

    cap = cv2.VideoCapture(source_path)

    # Object detection from stable camera
    object_detector = cv2.createBackgroundSubtractorMOG2(
                        history=100,
                        varThreshold=10)

    ret, img = cap.read()
    current_frame = 0
    ids = {}
    book = eu.book_initializer(system,ss)
    if visualize:
        cv2.namedWindow('img', cv2.WINDOW_NORMAL)

    while ret:
        if visualize:
            img_copy = img.copy()

        mask = object_detector.apply(img) # Básicamente la máscara es aplicar BackgroundSubstractor con 100 y 40 a toda la imagen

        _, mask = cv2.threshold( mask, 254, 255, # Se pasa la máscara por un threshold de grises
                                    cv2.THRESH_BINARY )
        contours, _ = cv2.findContours( mask, # Desde el resultado de esa máscara se sacan los contornos
                                        cv2.RETR_TREE,
                                        cv2.CHAIN_APPROX_SIMPLE )

        circle_contours = []
        for c in contours:
            area = cv2.contourArea(c)
            # Se comprueba que tenga cierto tamaño de area, y luego que, o bien el minimo circulo que se le pueda hacer al contorno alrededor tenga un area parecida,
            # o bien que la forma geometrica mas parecida al contorno tenga al menos 4 lados y sea convexo
            # Es decir, se intenta detectar una forma circular con cierta area
            if area > min_contour_area:
                _, radius = cv2.minEnclosingCircle(c)
                enclosing_area = np.pi * radius * radius
                approx = cv2.approxPolyDP(c,0.1*cv2.arcLength(c,True),True)
                if (len(approx)>3 and cv2.isContourConvex(approx)) or abs(area - enclosing_area) < enclosing_area_diff * enclosing_area:
                    circle_contours.append(contour_center(c))

        if len(circle_contours) > 0:
            if len(ids) == 0:
                # Creo los ids de cada contorno
                for c in circle_contours:
                    new_id_dict = kpu.init_id_dict(c)
                    ids[len(ids)] = new_id_dict
            else:
                kpu.update_ids(ids, circle_contours)
                # En caso de haber perdido alguna detección, la actualizo con su predicción
                kpu.update_lost_detections(ids)             

        for key in ids:
            elem = ids[key]
            coord = elem["Coord"]

            if coord != elem["Prediction"]:
                eu.book_writer(book, current_frame+1, key+1, coord)
                if coord is not None and visualize:
                    x1, y1 = elem["Coord"]
                    cv2.rectangle(img_copy, (int(x1 - 15), int(y1 - 15)), (int(x1 + 15), int(y1 + 15)), (0, 0, 255), 2)
                    cv2.putText(img_copy, "Id {}".format(key), (int(x1 + 15), int(y1 + 10)), 0, 0.5, (0, 0, 255), 2)

        ret, img = cap.read()
        current_frame += 1


        if visualize:
            cv2.imshow('img', img_copy)
            #cv2.imshow('img', cv2.resize(img, (480,700)))
            k=cv2.waitKey(0)
            if k==27: break

   

    if visualize:
            cap.release()
            cv2.destroyAllWindows()
    cap.release()

    print('finished tracking')        
    eu.book_saver(book,system,ss, sanitize=False)  #*edit*
    print('finished writing data with name' + f'.../tracking_{ss}_{system}.xlsx')

    return len(ids)


if __name__ == "__main__":
    source_path = '/home/alex/tfg_jugglingTrackingSiteswap/dataset/ss5_red_AlejandroAlonso.mp4'
    bg_substraction_tracking(source_path,visualize=True)
