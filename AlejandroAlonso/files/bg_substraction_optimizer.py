import concurrent.futures
import numpy as np
import math
from tracking.bg_substraction_tracking import bg_substraction_tracking
from metrics.motmetrics import motMetricsEnhancedCalculator
import random
def test(ss, min_area, enclosing_area, arc_const):
    # Esta es la función que se ejecutará con diferentes valores de 'param'
    source_path = '/home/alex/tfg_jugglingTrackingSiteswap/dataset/ss'+ss+'_red_AlejandroAlonso.mp4'
    res = bg_substraction_tracking(source_path,min_contour_area=min_area, enclosing_area_diff=enclosing_area, arc_const=arc_const, visualize=False, save_data=2)
    print(ss, min_area, enclosing_area, arc_const)
    return res

def main():
    """ siteswaps = ['1', '3', '441', '423', '5']
    min_areas = range(500,1500,250)
    enclosing_area_diffs = np.arange(0.1,1,0.2)
    arc_consts = np.arange(0.05, 0.15, 0.25) """
    siteswaps = ['3']
    min_areas = range(500,700,100)
    enclosing_area_diffs = np.arange(0.5,0.8,0.2)
    arc_consts = np.arange(0.1, 0.15, 0.25)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Para cada valor de 'param' creamos un objeto Future que ejecuta la función 'test'
        futures = {executor.submit(test, ss, min_area, enclosing_area, arc_const): (ss, min_area, enclosing_area, arc_const) for ss in siteswaps for min_area in min_areas for enclosing_area in enclosing_area_diffs for arc_const in arc_consts}

        # Esperamos a que todas las ejecuciones de la función 'test' terminen
        concurrent.futures.wait(futures)
        """ with open("/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/res_seq_optimizer.txt", "w") as f:
            for future in futures:
                f.write(f'{future.result()}\n') """

if __name__ == '__main__':
    main()
