import concurrent.futures
import numpy as np
from tracking.color_tracking_max_balls_optimizer import color_tracking_max_balls
from metrics.motmetrics import motMetricsEnhancedCalculator

def test(ss, dt, u_x, u_y, std_acc, x_std_meas, y_std_meas):
    # Esta es la función que se ejecutará con diferentes valores de 'param'
    # En este ejemplo simplemente se devuelve el valor de 'param' elevado al cuadrado
    max_balls = ss[1]
    source_path = '/home/alex/tfg_jugglingTrackingSiteswap/dataset/ss'+str(ss[0])+'_red_AlejandroAlonso.mp4'
    color_range = 35,30,150,185,120,255
    return color_tracking_max_balls(source_path, color_range, max_balls=max_balls, save_data=2, visualize=False, dt=dt, u_x=u_x, u_y=u_y, std_acc=std_acc, x_std_meas=x_std_meas, y_std_meas=y_std_meas)

def metric(res):
    ss, filename = res[0], res[1]
    gt_path = '/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/mot16/GroundTruth/'
    t_path = '/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/mot16/Optimizer/'
    print(filename)
    return motMetricsEnhancedCalculator(filename, gt_path+str(ss)+'_manual.txt', t_path+filename)

def main():
    # Lista de valores de 'param' que se utilizarán en las ejecuciones de la función 'test'
    #siteswaps = [(1,1), (3,3), (441,3), (423,3), (5,5)]
    siteswaps = [(3,3)]
    dts = np.arange(0.1, 0.3, 0.1)
    u_xs = range(15,40,5)
    u_ys = range(15,40,5)
    std_accs = range(15,40,5)
    x_std_meass = np.arange(0.1, 0.3, 0.1)
    y_std_meass = np.arange(0.1, 0.3, 0.1)

    # Creamos un objeto de tipo ThreadPoolExecutor para ejecutar las funciones en paralelo
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Para cada valor de 'param' creamos un objeto Future que ejecuta la función 'test'
        futures = {executor.submit(test, ss, dt, u_x, u_y, std_acc, x_std_meas, y_std_meas): (ss, dt, u_x, u_y, std_acc, x_std_meas, y_std_meas) for ss in siteswaps\
                    for dt in dts for u_x in u_xs for u_y in u_ys for std_acc in std_accs for x_std_meas in x_std_meass for y_std_meas in y_std_meass}

        # Esperamos a que todas las ejecuciones de la función 'test' terminen
        concurrent.futures.wait(futures)

        # Aplicamos la función de métrica 'metric' al resultado de cada ejecución de la función 'test'
        resultados = [metric(future.result()) for future in futures]

        # Guardamos los resultados en un archivo de texto con el formato 'param - resultado de la métrica'
        with open('/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/mot16/Optimizer/resultados.txt', 'w') as f:
            f.write("                                       T. Perdido  D. Perdidas  D. Ruido  ID swap  nBalls  <20%  20%80%  >80% Recall Precision   MOTA   MOTP\n")
            for resultado in resultados:
                f.write(f'{resultado}\n')


if __name__ == '__main__':
    main()
