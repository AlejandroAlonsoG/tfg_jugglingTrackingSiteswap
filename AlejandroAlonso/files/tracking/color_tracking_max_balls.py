# Import libraries
import cv2, numpy as np
try:
    import prediction.kalman_prediction_utils as kpu
    from preprocessing.color_extractor import color_extractor
    import data_saver_files.excel_utils as eu
    import data_saver_files.mot16_utils as mu
except:
    import tracking.prediction.kalman_prediction_utils as kpu
    from tracking.preprocessing.color_extractor import color_extractor
    import tracking.data_saver_files.excel_utils as eu
    import tracking.data_saver_files.mot16_utils as mu
import re

# Takes image and color, returns parts of image that are that color
def only_color(frame, hsv_range):
    (h,s,v,h1,s1,v1) = hsv_range
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # define range of blue color in HSV
    lower = np.array([h,s,v])
    upper = np.array([h1,s1,v1])
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower, upper)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)
    return res, mask

#takes an image and the threshold value returns the contours
def get_contours(im):
    imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    # cv2.threshold(src, threshold value, maximum value, type (0 binario creo))
    _ ,thresh = cv2.threshold(imgray,0,255,0)
    contours, _ = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #contours, _ = cv2.findContours(imgray,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    return contours

#finds the center of a contour
#takes a single contour
#returns (x,y) position of the contour
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

def color_tracking_max_balls(source_path, hsv_range, non_max_suppresion_threshold=39, max_balls=3, force_match=True, visualize=False, save_data=-1):
    system = "ColorTrackingMaxBalls"
    try:
        ss= re.search(r"ss(\d+)", source_path).group(1)
    except:
        ss="Unknown"
    h,s,v,h1,s1,v1 = hsv_range
    cap = cv2.VideoCapture(source_path)
    # Create list to save data
    frame_number= 0
    ids = {}
    if save_data==1:
        book = eu.book_initializer(system,ss)
    elif save_data==2:
        file = mu.file_initializer(system,ss,'Tracking')
    if visualize:
        cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    # Iterate though each frame of video
    while True:
        
        # Read image from the video
        _, img = cap.read()
        
        # Chech if the video is over
        try: l = img.shape
        except: break

        if visualize:
            img_copy = img.copy()
        
        # Segment the image by color
        img, _ = only_color(img, (h,s,v,h1,s1,v1))

        # Find the contours in the image
        contours = get_contours(img)

        # If there are contours found in the image:
        if len(contours)>0:
            contours = contours_non_max_suppression(contours, non_max_suppresion_threshold)
            # Saca los centros de los contornos para trabajar con ellos
            contours = [contour_center(c) for c in contours if contour_center(c) != (0,0)]
            if len(ids) == 0:
                #Si tengo mas detecciones que bolas quito las ultimas detecciones (TODO igual hay mejor forma, quitarlo en funcion de un roi o algo asi)
                contours = contours[:max_balls]
                # Creo los ids de cada contorno
                for c in contours:
                    new_id_dict = kpu.init_id_dict(c, frame_number)
                    ids[len(ids)] = new_id_dict
            else:
                # Actualizo los ids que tengo con las detecciones nuevas
                if len(contours) > 0:
                    kpu.update_ids(ids, contours, frame_number, max_balls=max_balls, force=force_match)
                # En caso de haber perdido alguna detección, la actualizo con su predicción
                kpu.update_lost_detections(ids)

            for key in ids:
                elem = ids[key]
                coord = elem["Coord"]

                if coord != elem["Prediction"]:
                    if save_data==1:
                        eu.book_writer(book, frame_number+1, key+1, coord)
                    elif save_data==2:
                        mu.file_writer(file, frame_number+1, key+1, coord)
                    if coord is not None and visualize:
                        x1, y1 = elem["Coord"]
                        cv2.rectangle(img_copy, (int(x1 - 15), int(y1 - 15)), (int(x1 + 15), int(y1 + 15)), (0, 0, 255), 2)
                        cv2.putText(img_copy, "Id {}".format(key), (int(x1 + 15), int(y1 + 10)), 0, 0.5, (0, 0, 255), 2)

        frame_number += 1
        #show the image and wait 1080x1920
        if visualize:
            cv2.imshow('img', img_copy)
            k=cv2.waitKey(1)
            if k==27: break
        
    #release the video to avoid memory leaks, and close the window
    if visualize:
        cap.release()
        cv2.destroyAllWindows()

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
    max_balls = 7
    #source_path = '/home/alex/tfg_jugglingTrackingSiteswap/dataset/jugglingLab/ss31_red_JugglingLab.mp4'
    source_path = '/home/alex/tfg_jugglingTrackingSiteswap/dataset/tanda2/ss7_red2_AlejandroAlonso.mp4'
    #color_range = 35,30,150,185,120,255
    color_range = 168,140,69,175,255,198 #red2_AlejandroAlonso to help with color_tracking
    #color_range = 0, 50, 0, 255, 255, 255
    #color_range = color_extractor(source_path)
    color_tracking_max_balls(source_path, color_range, max_balls=max_balls, save_data=2, visualize=True)