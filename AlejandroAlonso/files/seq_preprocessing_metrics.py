import math
from prettytable import PrettyTable
from prediction.seq_preprocessing import bg_substraction_tracking

def distancia_y_rango(punto, point_pred, umbral):
    """
    Calcula la distancia entre el punto dado y el punto (x,y),
    y determina si el punto está dentro del rango [(x-umbral,y-umbral),(x+umbral,y+umbral)].

    Argumentos:
    punto -- una tupla de dos valores representando las coordenadas del punto a analizar
    x -- el valor x del punto central
    y -- el valor y del punto central
    umbral -- el valor del umbral

    Retorna:
    Una tupla de dos elementos:
    - la distancia entre el punto dado y el punto (x,y)
    - un booleano indicando si el punto está dentro del rango especificado
    """
    x,y = point_pred
    # Calcula la distancia entre el punto dado y el punto (x,y)
    distancia = math.sqrt((punto[0]-x)**2 + (punto[1]-y)**2)

    # Determina si el punto está dentro del rango [(x-umbral,y-umbral),(x+umbral,y+umbral)]
    dentro_del_rango = (punto[0] >= x-umbral) and (punto[0] <= x+umbral) and (punto[1] >= y-umbral) and (punto[1] <= y+umbral)

    # Retorna una tupla con la distancia y si está dentro del rango
    return (distancia, dentro_del_rango)

# Distancia respecto al punto GT y si el punto está en cierto rango

if __name__ == "__main__":
    siteswaps = [('1', [557,900]),
                 ('3', [580,950]),
                 ('441', [550,970]),
                 ('423', [570,972]),
                 ('5', [560,820])]
    
    table = PrettyTable()
    table.field_names = ["ss", "gt", "pred", "dist", "in_range"]
    for ss, point_gt in siteswaps:
        source_path = '/home/alex/tfg_jugglingTrackingSiteswap/dataset/ss'+ss+'_red_AlejandroAlonso.mp4'
        point_pred = bg_substraction_tracking(source_path,convergence_threshold=1, visualize=False)
        dist, in_range = distancia_y_rango(point_gt, point_pred, 30)
        table.add_row([ss, point_gt, point_pred, dist, in_range])

    print(table)