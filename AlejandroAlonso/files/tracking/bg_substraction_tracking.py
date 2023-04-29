import cv2
import numpy as np
import re
try:
    import tracking.prediction.kalman_prediction_utils as kpu
except:
    import prediction.kalman_prediction_utils as kpu
try:
    import data_saver_files.excel_utils as eu
    import data_saver_files.mot16_utils as mu
except:
    import tracking.data_saver_files.excel_utils as eu
    import tracking.data_saver_files.mot16_utils as mu

def contour_center(c):
    M = cv2.moments(c)
    try: center = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
    except: center = 0,0
    return center


# Pilla el color más detectado y hace un rango desde ahi
def get_division_point(source_path, min_contour_area=1000, enclosing_area_diff=0.5, arc_const=0.1, save_data=-1, visualize=False):
    try:
        ss= re.search(r"ss(\d+)", source_path).group(1)
    except:
        ss="Unknown"
    system = "BgSubstractionTracking"

    cap = cv2.VideoCapture(source_path)

    # Object detection from stable camera
    object_detector = cv2.createBackgroundSubtractorMOG2(
                        history=100,
                        varThreshold=10)

    ret, img = cap.read()
    current_frame = 0
    ids = {}
    if save_data==1:
        book = eu.book_initializer(system,ss) #*edit*
    elif save_data==2:
        file = mu.file_initializer(system,ss,'Tracking')
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
                approx = cv2.approxPolyDP(c,arc_const*cv2.arcLength(c,True),True)
                if (len(approx)>3 and cv2.isContourConvex(approx)) or abs(area - enclosing_area) < enclosing_area_diff * enclosing_area:
                    circle_contours.append(contour_center(c))

        if len(circle_contours) > 0:
            if len(ids) == 0:
                # Creo los ids de cada contorno
                for c in circle_contours:
                    new_id_dict = kpu.init_id_dict(c, current_frame, dt=0.1, u_x=15, u_y=30, std_acc=30, x_std_meas=0.1, y_std_meas=0.1)
                    ids[len(ids)] = new_id_dict
            else:
                kpu.update_ids(ids, circle_contours, current_frame, dt=0.1, u_x=15, u_y=30, std_acc=30, x_std_meas=0.1, y_std_meas=0.1)
                # En caso de haber perdido alguna detección, la actualizo con su predicción
                kpu.update_lost_detections(ids)             

        for key in ids:
            elem = ids[key]
            coord = elem["Coord"]

            if coord != elem["Prediction"]:
                if save_data==1:
                    eu.book_writer(book, current_frame+1, key+1, coord)
                elif save_data==2:
                    mu.file_writer(file, current_frame+1, key+1, coord)
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

    if save_data==1:
        print('finished tracking')        
        eu.book_saver(book,system,ss, sanitize=False)  #*edit*
        print('finished writing data with name' + f'.../tracking_{ss}_{system}.xlsx')
    elif save_data==2:
        print('finished tracking')        
        mu.file_saver(file)

    ret_ids = {}
    for key in ids:
        ids[key]["Hist"].append(ids[key]["Coord"])
        elem = {}
        x_coords, y_coords = [], []
        for c in ids[key]["Hist"]:
            if c != None:
                x_coords.append(c[0])
                y_coords.append(c[1])
            else:
                x_coords.append(None)
                y_coords.append(None)
        elem["x"] = x_coords
        elem["y"] = y_coords
        elem["Start"] = ids[key]["Start"]
        ret_ids[key] = elem

    return ret_ids


if __name__ == "__main__":
    source_path = '/home/alex/tfg_jugglingTrackingSiteswap/dataset/tanda2/ss441_red2_AlejandroAlonso.mp4'
    get_division_point(source_path,visualize=False, save_data=2)
