import concurrent.futures
import numpy as np
import math
from tracking.bg_substraction_tracking_max_balls import bg_substraction_tracking_max_balls
from metrics.motmetrics import motMetricsEnhancedCalculator
import random
def test(ss, min_area, enclosing_area, arc_const):
    # Esta es la función que se ejecutará con diferentes valores de 'param'
    source_path = './dataset/ss'+ss[0]+'_red_AlejandroAlonso.mp4'
    res = bg_substraction_tracking_max_balls(source_path,min_contour_area=min_area, enclosing_area_diff=enclosing_area, arc_const=arc_const, max_balls=ss[1], visualize=False, save_data=2)
    print(ss, min_area, enclosing_area, arc_const)
    return res

def main():
    siteswaps = [('1',1), ('3',3), ('441',3), ('423',3), ('5',5)]
    min_areas = range(1900,2500,250)
    enclosing_area_diffs = np.arange(1,1.51,0.1)
    arc_consts = np.arange(0.08, 0.12, 0.1)
    """ siteswaps = ['3']
    min_areas = range(500,700,100)
    enclosing_area_diffs = np.arange(0.5,0.8,0.2)
    arc_consts = np.arange(0.1, 0.15, 0.25) """

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Para cada valor de 'param' creamos un objeto Future que ejecuta la función 'test'
        futures = {executor.submit(test, ss, min_area, enclosing_area, arc_const): (ss, min_area, enclosing_area, arc_const) for ss in siteswaps for min_area in min_areas for enclosing_area in enclosing_area_diffs for arc_const in arc_consts}

        # Esperamos a que todas las ejecuciones de la función 'test' terminen
        concurrent.futures.wait(futures)
        """ with open("./AlejandroAlonso/results/res_seq_optimizer.txt", "w") as f:
            for future in futures:
                f.write(f'{future.result()}\n') """

if __name__ == '__main__':
    main()
