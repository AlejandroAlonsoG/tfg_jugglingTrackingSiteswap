try:
    from tracking.prediction.kalman_filter import KalmanFilter
except:
    from prediction.kalman_filter import KalmanFilter
import numpy as np
import math

def init_id_dict(measure, first_frame, dt=0.3, u_x=1, u_y=1, std_acc=8.5, x_std_meas=0.1, y_std_meas=0.1):
    measure_data = {}
    measure_data["Coord"] = measure
    measure_data["Hist"] = []
    KF = KalmanFilter(dt, u_x,u_y, std_acc, x_std_meas, y_std_meas)
    KF.update(np.array([[measure[0]], [measure[1]]]))
    measure_data["KalmanFilter"] = KF
    # Dado que la primera prediccion no es precisa se guarda las coordenadas
    measure_data["Prediction"] = measure
    measure_data["HistPrediction"] = []
    measure_data["Matched"] = False
    measure_data["Start"] = first_frame
    return measure_data

# TODO valorar si puede compensar pasar una lista con las predicciones de los ids en vez de toda la estructura
def create_distance_matrix(ids, measure_list):
    dist_matrix = np.zeros((len(measure_list),len(ids)))

    for idx,key in enumerate(ids):
        for jdx, curr_c in enumerate(measure_list):
            prev_center = ids[key]["Prediction"]
            if curr_c is None:
                dist_matrix[jdx,idx] = -1
            else:
                curr_dist =  math.dist(prev_center, curr_c)
                dist_matrix[jdx,idx] = curr_dist

    return dist_matrix

def update_ids(ids, measure_list, curr_frame, max_balls=128, limit_dist=2000, force=False, dt=0.3, u_x=1, u_y=1, std_acc=8.5, x_std_meas=0.1, y_std_meas=0.1):
    dist_matrix = create_distance_matrix(ids, measure_list)

    #Asignar según la distancia de la matriz sea mínima
    max_dist = np.max(dist_matrix)
    #Queremos encontrar todas las coincidencias por debajo de la distancia maxima
    for _ in range(len(measure_list)):
        min_dist = dist_matrix.argmin()
        # Coords de la distancia minima en toda la matriz
        min_value_index = np.unravel_index(min_dist, dist_matrix.shape)
        # Como la matriz es coords_nuevas \ coords_antiguas, sacamos los indices
        measure_list_index = min_value_index[0]
        ids_index = min_value_index[1]
        # Haces la asignación
        if 0 <= dist_matrix[measure_list_index,ids_index] <= limit_dist and max_dist+1 != np.min(dist_matrix):
            # Guardo la coordenada en el historial
            ids[ids_index]["Hist"].append(ids[ids_index]["Coord"])
            # Asigno la nueva coordenada
            ids[ids_index]["Coord"] = measure_list[measure_list_index]
            # Actualizo el filtro de Kalman
            ids[ids_index]["KalmanFilter"].update(np.array([[measure_list[measure_list_index][0]], [measure_list[measure_list_index][1]]]))
            # Reinicio el historial de predicciones
            new_predictions = []
            new_predictions.append(ids[ids_index]["Prediction"])
            ids[ids_index]["HistPrediction"] = new_predictions
            # Hago la nueva prediccion
            (x,y) = ids[ids_index]["KalmanFilter"].predict()
            ids[ids_index]["Prediction"] = (x.max(),y.max())
            # Lo marco como encontrado
            ids[ids_index]["Matched"] = True
        # Creas nuevo id si hay ids disponibles
        elif dist_matrix[measure_list_index,ids_index] > 0 and len(ids) < max_balls:
            new_id_dict = init_id_dict(measure_list[measure_list_index], curr_frame, dt=dt, u_x=u_x, u_y=u_y, std_acc=std_acc, x_std_meas=x_std_meas, y_std_meas=y_std_meas)
            ids[len(ids)] = new_id_dict
        # Si quedan asignaciones por hacer y tienes el flag de forzarlas las haces aunque esten lejos del limite
        elif dist_matrix[measure_list_index,ids_index] > 0 and max_dist+1 != np.min(dist_matrix) and force==True:
            # Guardo la coordenada en el historial
            ids[ids_index]["Hist"].append(ids[ids_index]["Coord"])
            # Asigno la nueva coordenada
            ids[ids_index]["Coord"] = measure_list[measure_list_index]
            # Actualizo el filtro de Kalman
            ids[ids_index]["KalmanFilter"].update(np.array([[measure_list[measure_list_index][0]], [measure_list[measure_list_index][1]]]))
            # Reinicio el historial de predicciones
            new_predictions = []
            new_predictions.append(ids[ids_index]["Prediction"])
            ids[ids_index]["HistPrediction"] = new_predictions
            # Hago la nueva prediccion
            (x,y) = ids[ids_index]["KalmanFilter"].predict()
            ids[ids_index]["Prediction"] = (x.max(),y.max())
            # Lo marco como encontrado
            ids[ids_index]["Matched"] = True
        # Resto de las detecciones las pierdes

        
        # Quitas tanto el id como la deteccion para futuras asignaciones, si las coordenadas
        # eran None simplemente quitas esa fila
        if dist_matrix[measure_list_index,ids_index] == -1:
            dist_matrix[measure_list_index,:] = max_dist+1
        else:
            dist_matrix[measure_list_index,:] = max_dist+1
            dist_matrix[:,ids_index] = max_dist+1

    # TODO valorar si tengo que devolver los ids o se actualizan solos por referencia


def update_lost_detections(ids, accumulate_predictions_limit = 10):
    for key in ids:
        elem = ids[key]
        if elem["Matched"] == False:
            if len(elem["HistPrediction"])<=accumulate_predictions_limit:

                # Guardo la coordenada en el historial
                elem["Hist"].append(elem["Coord"])
                (x,y) = elem["KalmanFilter"].predict()
                # Predict devuelve una matriz por coordenada con solo ese valor, por lo que lo extraemos
                x = x.max()
                y = y.max()
                if x > 0 and y > 0:
                    # Asigno la prediccion como nueva coordenada
                    elem["Coord"] = (x,y)
                    # Actualizo el filtro de Kalman
                    elem["KalmanFilter"].update(np.array([[x], [y]]))
                    # Guardo la última predicción en el historial
                    elem["HistPrediction"].append(elem["Prediction"])
                    # Hago la nueva prediccion
                    elem["Prediction"] = (x,y)
                else:
                    # Asigno None como coordenada
                    elem["Coord"] = None
                    # Actualizo el filtro de Kalman
                    elem["KalmanFilter"].update(np.array([[x], [y]]))
                    # Guardo la última predicción en el historial
                    elem["HistPrediction"].append(elem["Prediction"])
                    # Hago la nueva prediccion
                    elem["Prediction"] = (x,y)
            else:
                # Asigno None como coordenada
                elem["Coord"] = None
        # Lo dejo en falso para siguientes iteraciones
        else:
            elem["Matched"] = False
    
    # TODO valorar si tengo que devolver los ids o se actualizan solos por referencia
