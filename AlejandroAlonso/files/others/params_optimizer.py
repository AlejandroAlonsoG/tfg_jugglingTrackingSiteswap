import concurrent.futures
import numpy as np
import math
from prediction.seq_preprocessing import get_division_point
from metrics.motmetrics import motMetricsEnhancedCalculator
import random
def test(ss, threshold):
    # Esta es la función que se ejecutará con diferentes valores de 'param'
    source_path = '/home/alex/tfg_jugglingTrackingSiteswap/dataset/ss'+str(ss[0])+'_red_AlejandroAlonso.mp4'
    res,_ = get_division_point(source_path,convergence_threshold=1, x_mul_threshold=threshold,  visualize=False)
    res1 = res >= ss[1][0] and res <= ss[1][0]
    res2 = abs(((ss[1][1]-ss[1][0]) //2) - res)
    print("{}\t{}\t{}\t{}\t{}".format(ss, threshold, res, res1, res2))
    return "{}\t{}\t{}\t{}\t{}".format(ss, threshold, res, res1, res2)

def main():
    # Lista de valores de 'param' que se utilizarán en las ejecuciones de la función 'test'
    siteswaps = [(1,(482,632)), (3,(570,600)), (441,(530,557)), (423,(555,590)), (5,(545, 575))]
    #siteswaps = [(3,(570,600)),]
    theshold = [1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.01]
    #theshold = [0.6,]
    # Creamos un objeto de tipo ThreadPoolExecutor para ejecutar las funciones en paralelo
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Para cada valor de 'param' creamos un objeto Future que ejecuta la función 'test'
        futures = {executor.submit(test, ss, theshold_value): (ss, theshold_value) for ss in siteswaps for theshold_value in theshold}

        # Esperamos a que todas las ejecuciones de la función 'test' terminen
        concurrent.futures.wait(futures)
        with open("/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/res_seq_optimizer.txt", "w") as f:
            for future in futures:
                f.write(f'{future.result()}\n')

if __name__ == '__main__':
    main()
