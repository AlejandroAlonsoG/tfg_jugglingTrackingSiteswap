from kalman_filter import KalmanFilter
import numpy as np
import cv2

measures =[
    [(518,1229), (534,1299), (655,1211)],
    [(515,1252), (526,1227), (663,1221)],
    [(516,1247), (525,1227), (665,1209)],
    [(516,1250), (526,1227), (660,1188)],
    [(516,1253), (528,1227), (656,1163)],
    [(518,1252), (529,1226), (657,1149)],
    [(521,1249), (531,1223), (658,1143)],
    [(528,1237), (537,1212), (659,1136)],
    [(534,1216), (540,1195), (663,1133)],
    [(538,1185), (540,1187), (667,1141)],
    [(542,1154), (543,1167), (670,1152)],
    [(544,1078), (542,1112), (668,1162)],
    [(550,1011), (544,1073), (666,1174)],
    [(558,965), (544,1055), (664,1185)],
    [(564,932), (543,1045), (662,1196)],
    [(569,899), (543,1033), (658,1210)],
    [(571,864), (543,1023), (650,1223)],
    [(573,829), (539,1041), (647,1228)],
    [(580,804), (533,1064), (646,1222)],
    [(590,791), (532,1074), (645,1220)],
    [(599,780), (529,1088), (637,1211)],
    [(608,779), (527,1099), (620,1184)],
    [(618,785), (525,1112), (605,1144)],
    [(628,792), (523,1131), (592,1106)],
    [(635,803), (521,1152), (585,1063)],
    [(639,823), (518,1176), (580,1009)],
    [(644,849), (524,1183), (575,955)],
    [(654,876), (526,1204), (571,924)],
    [(665,904), (528,1225), (564,897)],
    [(676,936), (532,1239), (556,870)],
    [(686,974), (538,1241), (546,845)],
    [(693,1008), (543,1220), (536,826)],
    [(701,1037), (553,1199), (532,826)],
    [(707,1057), (564,1183), (526,835)],
    [(708,1073), (574,1157), (521,823)],
    [(712,1093), (590,1103), (513,830)],
    [(709,1116), (595,1038), (505,839)],
    [(694,1136), (596,983), (501,856)],
    [(681,1155), (596,936), (500,881)],
    [(671,1172), (594,892), (498,908)],
    [(664,1190), (592,862), (495,938)],
    [(659,1206), (593,832), (492,970)],
    [(655,1215), (599,803), (490,1004)],
    [(647,1217), (603,785), (489,1030)],
    [(644,1223), (607,769), (482,1051)],
    [(635,1222), (610,754), (480,1062)],
    [(621,1197), (612,754), (479,1070)],
    [(606,1162), (615,763), (479,1084)],
    [(598,1136), (620,777), (479,1100)],
    [(588,1095), (626,792), (487,1117)],
    [(583,1042), (628,809), (492,1142)],
    [(578,989), (629,830), (497,1167)],
    [(573,939), (632,854), (504,1182)],
    [(569,902), (638,883), (501,1201)],
    [(565,882), (642,926), (501,1222)],
    [(560,862), (649,964), (504,1241)],
    [(554,838), (658,985), (509,1249)],
    [(548,814), (666,989), (517,1234)],
    [(546,797), (673,1000), (530,1218)],
    [(542,788), (680,1011), (546,1201)],
    [(536,793), (687,1024), (567,1180)],
    [(530,802), (691,1044), (588,1156)],
    [(527,816), (695,1065), (594,1102)],
    [(524,835), (699,1089), (595,1038)],
    [(522,858), (701,1115), (597,970)],
    [(519,885), (700,1142), (600,924)]
]
 
dt, u_x,u_y, std_acc, x_std_meas, y_std_meas = 0.1, 10, 10, 10, 0.1, 0.1
cv2.namedWindow('img', cv2.WINDOW_NORMAL)
ids = {}
for measure_list in measures:
    if len(ids) == 0:
        for measure in measure_list:
            measure_data = {}
            measure_data["Coord"] = measure
            measure_data["Hist"] = []
            KF = KalmanFilter(dt, u_x,u_y, std_acc, x_std_meas, y_std_meas)
            (x,y) = KF.predict()
            measure_data["KalmanFilter"] = KF
            # Dado que la primera prediccion no es precisa se guarda las coordenadas
            measure_data["Prediction"] = measure
            measure_data["HistPrediction"] = []
            measure_data["Matched"] = False
            ids[len(ids)] = measure_data
    else:
        # Crear matriz de distancias
        dist_matrix = np.zeros((len(ids),len(measure_list)))

        for idx,prev_c in enumerate(ids):
            for jdx, curr_c in enumerate(measure_list):
                prev_center = ids[idx]["Prediction"]
                curr_center = measure_list[jdx]
                curr_dist = np.linalg.norm(np.array(prev_center) - np.array(curr_center))
                dist_matrix[jdx,idx] = curr_dist
        
        #Asignar según la distancia de la matriz sea mínima
        limit_dist = 100 # TODO sacar parametro
        max_dist = dist_matrix.max()
        #Queremos encontrar todas las coincidencias por debajo de la distancia maxima
        for i in range(len(measure_list)):
            min_dist = dist_matrix.argmin()
            # Coords de la distancia minima en toda la matriz
            min_value_index = np.unravel_index(min_dist, dist_matrix.shape)
            # Quitas tanto el id como la deteccion para futuras asignaciones
            dist_matrix[min_value_index[0],:] = max_dist+1
            dist_matrix[:,min_value_index[1]] = max_dist+1
            # Haces la asignación
            if min_dist <= limit_dist:
                # TODO Comprobar que es min_value_index[0] y no de [1]
                # Guardo la coordenada en el historial
                ids[min_value_index[0]]["Hist"].append(ids[min_value_index[0]]["Coord"])
                # Asigno la nueva coordenada
                ids[min_value_index[0]]["Coord"] = measure_list[min_value_index[1]]
                # Actualizo el filtro de Kalman
                ids[min_value_index[0]]["KalmanFilter"].update(np.array([[measure_list[min_value_index[1]][0]], [measure_list[min_value_index[1]][1]]]))
                # Reinicio el historial de predicciones
                new_predictions = []
                new_predictions.append(ids[min_value_index[0]]["Prediction"])
                ids[min_value_index[0]]["HistPrediction"] = new_predictions
                # Hago la nueva prediccion
                ids[min_value_index[0]]["Prediction"] = ids[min_value_index[0]]["KalmanFilter"].predict()
                # Lo marco como encontrado
                ids[min_value_index[0]]["Matched"] = True
            # Creas nuevo id
            else:
                measure_data = {}
                measure_data["Coord"] = measure_list[min_value_index[1]]
                measure_data["Hist"] = []
                KF = KalmanFilter(dt, u_x,u_y, std_acc, x_std_meas, y_std_meas)
                (x,y) = KF.predict()
                measure_data["KalmanFilter"] = KF
                # Dado que la primera prediccion no es precisa se guarda las coordenadas
                measure_data["Prediction"] = measure_list[min_value_index[1]]
                measure_data["HistPrediction"] = []
                measure_data["Matched"] = False
                ids[len(ids)] = measure_data

        # Actualizar detecciones perdidas
        accumulate_predictions_limit = 10 # TODO sacar parametro
        for key in ids:
            elem = ids[key]
            if elem["Matched"] == False:
                if len(elem["HistPrediction"]<accumulate_predictions_limit):
                    (x,y) = elem["KalmanFilter"].predict()
                    # Guardo la coordenada en el historial
                    elem["Hist"].append(elem["Coord"])
                    # Asigno la prediccion como nueva coordenada
                    elem["Coord"] = (x,y)
                    # Actualizo el filtro de Kalman
                    ids[min_value_index[0]]["KalmanFilter"].update(np.array([[x], [y]]))
                    # Guardo la última predicción en el historial
                    ids[min_value_index[0]]["HistPrediction"].append(ids[min_value_index[0]]["Prediction"])
                    # Hago la nueva prediccion
                    ids[min_value_index[0]]["Prediction"] = (x,y)
            # Lo dejo en falso para siguientes iteraciones
            else:
                elem["Matched"] = False


    height, width = 1920, 1080
    img = np.zeros((height, width, 3), np.uint8)
    img[:, :] = [255, 255, 255]

    for idx, measure in enumerate(measure_list):
        cv2.circle(img, measure, 10, (0, 255, 0), 2)
        cv2.putText(img, "Measure {}".format(idx), measure, 0, 0.5, (0, 0, 255), 2)
    
    for key in ids:
        elem = ids[key]
        x1, y1 = elem["Prediction"]
        cv2.rectangle(img, (int(x1 - 15), int(y1 - 15)), (int(x1 + 15), int(y1 + 15)), (0, 0, 255), 2)
        cv2.putText(img, "Assignment {}".format(key), (int(x1 + 15), int(y1 + 10)), 0, 0.5, (0, 0, 255), 2)
    
    #img = cv2.resize(img, (960, 540))
    cv2.imshow('img', img)
    cv2.waitKey(0)

cv2.destroyAllWindows() 