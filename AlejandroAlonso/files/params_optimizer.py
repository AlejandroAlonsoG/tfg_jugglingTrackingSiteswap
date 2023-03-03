import concurrent.futures
import numpy as np
from tracking.color_tracking_max_balls_optimizer import color_tracking_max_balls
from metrics.motmetrics import motMetricsEnhancedCalculator
import random
def test(ss, dist):
    # Esta es la función que se ejecutará con diferentes valores de 'param'
    # En este ejemplo simplemente se devuelve el valor de 'param' elevado al cuadrado
    max_balls = ss[1]
    print(dist)
    gt_path = '/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/mot16/GroundTruth/'
    source_path = '/home/alex/tfg_jugglingTrackingSiteswap/dataset/ss'+str(ss[0])+'_red_AlejandroAlonso.mp4'
    track_path = '/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/mot16/Optimizer/'
    color_range = 35,30,150,185,120,255
    color_tracking_max_balls(source_path, color_range, max_balls=max_balls, save_data=2, visualize=False, non_max_suppresion_threshold=dist)
    return motMetricsEnhancedCalculator(str(ss[0]), gt_path+str(ss[0])+'_manual.txt', track_path+str(ss[0])+"_ColorTracking_"+str(dist)+".txt")

def main():
    # Lista de valores de 'param' que se utilizarán en las ejecuciones de la función 'test'
    siteswaps = [(1,1), (3,3), (441,3), (423,3), (5,5)]
    dists = range(1,200,1)
    print(dists)
    # Creamos un objeto de tipo ThreadPoolExecutor para ejecutar las funciones en paralelo
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Para cada valor de 'param' creamos un objeto Future que ejecuta la función 'test'
        futures = {executor.submit(test, ss, dist): (ss, dist) for ss in siteswaps for dist in dists}

        # Esperamos a que todas las ejecuciones de la función 'test' terminen
        concurrent.futures.wait(futures)

        # Escribir los resultados a un fichero "res_concretos.txt" con formato: ss -> result
        with open("/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/mot16/Optimizer/res_distancia.txt", "w") as f:
            f.write("                                       T. Perdido  D. Perdidas  D. Ruido  ID swap  nBalls  <20%  20%80%  >80% Recall Precision   MOTA   MOTP\n")
            for future in futures:
                f.write(f'{future.result()}\n')

if __name__ == '__main__':
    main()
