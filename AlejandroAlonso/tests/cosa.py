import cv2
import numpy as np
import matplotlib.pyplot as plt

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

def contour_center(c):
    M = cv2.moments(c)
    try: center = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
    except: center = 0,0
    return center


def RellenarContornos(contours):
    filled_contours = []

    for contour in contours:
        # Obtener el contorno relleno como una lista de puntos
        filled_contour = cv2.approxPolyDP(contour, 3, True)

        # Agregar el punto inicial al final de la lista para cerrar el contorno
        filled_contour = np.concatenate((filled_contour, filled_contour[0].reshape(1, -1)))

        # Agregar el contorno relleno a la lista de contornos rellenos
        filled_contours.append(filled_contour)

    return filled_contours


# Pilla el color más detectado y hace un rango desde ahi
def bg_substraction_tracking(source_path, min_contour_area=1000,visualize=False):
    cap = cv2.VideoCapture(source_path)

    # Object detection from stable camera
    object_detector = cv2.createBackgroundSubtractorMOG2(
                        history=100,
                        varThreshold=10)

    if visualize:
        cv2.namedWindow('img', cv2.WINDOW_NORMAL)

    ret, img = cap.read()
    hist = None

    max_x, max_y = cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    bins = (int(max_x), int(max_y))
    hist_range = [(0, max_x), (0, max_y)]


    while ret:
        if visualize:
            img_copy = img.copy()

        mask = object_detector.apply(img) # Básicamente la máscara es aplicar BackgroundSubstractor con 100 y 40 a toda la imagen

        _, mask = cv2.threshold( mask, 254, 255, # Se pasa la máscara por un threshold de grises
                                    cv2.THRESH_BINARY )
        contours, _ = cv2.findContours( mask, # Desde el resultado de esa máscara se sacan los contornos
                                        cv2.RETR_TREE,
                                        cv2.CHAIN_APPROX_SIMPLE )
        true_contours = []
        for c in contours:
            area = cv2.contourArea(c)
            if area > min_contour_area:
                true_contours.append(c)
        true_contours = contours_non_max_suppression(true_contours, 39)
        coords = []
        for cnt in true_contours:
            if visualize:
                cv2.drawContours(img_copy, [cnt], 0, (0, 0, 255), 2)
            mask = np.zeros_like(img)
            cv2.fillPoly(mask, [cnt], 255)
            pts = np.where(mask == 255)
            for i in range(len(pts[0])):
                coords.append((pts[1][i], pts[0][i]))
                if visualize:
                    x1, y1 = pts[1][i], pts[0][i]
                    cv2.circle(img_copy, (x1, y1), 0, (0, 0, 255), 2)

        if len(coords) > 0:
            x_coords, y_coords = zip(*coords)
    
            hist_frame, xedges, yedges = np.histogram2d(x_coords, y_coords, bins=bins, range=hist_range)
            if hist is None:
                hist = hist_frame
            else:
                hist += hist_frame    

        if visualize:
            cv2.imshow('img', img_copy)
            #cv2.imshow('img', cv2.resize(img, (480,700)))
            k=cv2.waitKey(1)
            if k==27: break
        ret, img = cap.read()


    cap.release()
    if visualize:
        cap.release()
        cv2.destroyAllWindows()

    # Se obtiene el punto del eje x en el que se separan los dos clusters de detecciones
    column_sums = np.sum(hist, axis=1)
    high_zones = []
    start_idx = None
    x_threshold_mul = 0.6
    while x_threshold_mul > 0 and len(high_zones) != 2:
        threshold = column_sums.max()*x_threshold_mul # Igual se puede ir cambiando hasta dejar de tener 2
        for i, x in enumerate(column_sums):
            if x > threshold:
                if start_idx is None:
                    start_idx = i
            elif start_idx is not None:
                high_zones.append((start_idx, i-1))
                start_idx = None
        if start_idx is not None:
            high_zones.append((start_idx, len(column_sums)-1))
        x_threshold_mul -= 1

    if len(high_zones)>1:
        high_zones = sorted(high_zones, key = lambda sub: abs(sub[1] - sub[0]), reverse=True)[:2]
        x_mid_point = ( (high_zones[0][0]+high_zones[0][1])//2 + (high_zones[1][0]+high_zones[1][1])//2 ) //2
    else:
        print("No se ha encontrado los dos clusters del heatmap")
        x_mid_point = hist_range[0][1]//2
    # crear el mapa de calor con imshow
    print(column_sums.max())
   
    # Se obtiene el punto del eje y que marca la zona superior de los clusters
    row_sums = np.sum(hist, axis=0)
    threshold = row_sums.max()*0.6
    y_mid_point = 0
    for i, value in enumerate(row_sums):
        if value >= threshold:
            y_mid_point = i
            break
    y_mid_point = hist_range[1][1]- y_mid_point
    print(x_mid_point, y_mid_point)

    #plt.imshow(arr, cmap='hot', interpolation='nearest')
    plt.imshow(hist.T, origin='upper', extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]])
    plt.axvline(x=x_mid_point, color='r', linestyle='--')
    plt.axhline(y=y_mid_point, color='r', linestyle='--')
    plt.colorbar()
    plt.title('Mapa de calor del movimiento en el video')
    plt.show()

    return x_mid_point, y_mid_point


if __name__ == "__main__":
    source_path = '/home/alex/tfg_jugglingTrackingSiteswap/dataset/ss5_red_AlejandroAlonso.mp4'
    bg_substraction_tracking(source_path,visualize=False)
    # TODO limitar el tiempo, por ejemplo los 10 segundos del medio o algo así
