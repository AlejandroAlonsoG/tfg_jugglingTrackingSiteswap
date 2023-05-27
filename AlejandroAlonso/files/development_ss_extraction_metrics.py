from tracking.preprocessing.color_extractor import color_extractor
from tracking.color_tracking_max_balls import color_tracking_max_balls
from tracking.color_tracking_v0 import color_tracking
from tracking.bg_substraction_tracking_max_balls import bg_substraction_tracking_max_balls
from tracking.bg_substraction_tracking import bg_substraction_tracking
from prediction.seq_extractor_tmp import seq_extraction, seq_extraction_cuadrants
from prediction.ss_prediction_tmp import prediction, get_full_ss_string
from prediction.seq_preprocessing import point_extractor
from prettytable import PrettyTable
from tracking.data_saver_files.mot16_utils import load_data 
import concurrent.futures

# CONSTANTS
gt_dir = '/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/mot16/GroundTruth/'
tracking_dir = '/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/mot16/Tracking/'
dataset_dir = '/home/alex/tfg_jugglingTrackingSiteswap/dataset/tanda2/'
#dataset_dir = '/home/alex/tfg_jugglingTrackingSiteswap/dataset/jugglingLab/'
video_file_format = 'ss{}_red2_AlejandroAlonso.mp4' # ss
#video_file_format = 'ss{}_red_JugglingLab.mp4' # ss
gt_file_format = "{}_manual2.txt" # ss
tracking_file_format = '{}_{}.txt' # ss, tracking_system

def eq_ss(str1, str2):
    if len(str1) != len(str2):
        return False
    else:
        str1_str1 = str1 + str1
        return str2 in str1_str1

def execute(tracking_system = "",pred_system = "", max_balls = None, ss_test_numbers = 5, decimal_round=3, ss=None):
            source_path = dataset_dir + video_file_format.format(ss)

            if tracking_system == "Manual":
                file_path = gt_dir+gt_file_format.format(ss)
            elif tracking_system in ['ColorTrackingMaxBalls', 'ColorTrackingV0', 'BgSubstractionMaxBalls', 'BgSubstractionV0']:
                file_path = tracking_dir+tracking_file_format.format(ss, tracking_system)
            else:
                raise Exception("Wrong tracking system")

            ids = load_data(file_path)

            if pred_system == "Coords":
                throw_seq = seq_extraction(ids)
                num_misses = "---"
            elif pred_system == "Cuadrants":
                point = point_extractor(source_path)
                throw_seq, num_misses = seq_extraction_cuadrants(ids, point, 0,0)
            else:
                raise Exception("Wrong prediction system")
            ss_pred, full_ss = prediction(throw_seq, num_balls=max_balls, test_numbers=ss_test_numbers)
            print("Terminado: ", ss)
            present = ss_pred in ss or eq_ss(ss_pred, ss)
            presence = full_ss.count(ss)/(len(full_ss)/len(ss))
            period = len(ss_pred) == len(ss)
            works = eq_ss(ss_pred, ss)
            return ss, ss_pred, present, round(presence, decimal_round), period, round(num_misses, decimal_round), works


if __name__ == "__main__":
    #siteswaps = ['1', '40', '31', '4', '330', '3', '423', '441', '531', '51', '633', '5551', '525', '534', '66611', '561', '75314', '5', '645', '744', '91', '6']
    siteswaps = ['1', '3', '423', '441', '5']
    tracking_systems = ['Manual','ColorTrackingMaxBalls', 'ColorTrackingV0', 'BgSubstractionMaxBalls', 'BgSubstractionV0']
    prediction_systems = ['Coords', 'Cuadrants']
    table = PrettyTable()
    table.field_names = ["ss", "Predicción", "Presente", "Presencia general", "Periodo", "Fallos", "Coincide"]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Para cada valor de 'param' creamos un objeto Future que ejecuta la función 'test'
        futures = {executor.submit(execute, tracking_systems[0], prediction_systems[1], int(sum(int(char) for char in ss) / len(ss)), 5, 3, ss): (ss) for ss in siteswaps}

        # Esperamos a que todas las ejecuciones de la función 'test' terminen
        concurrent.futures.wait(futures)
    
    for future in futures:
        table.add_row(future.result())
    print(table)

    """ for idx, ss in enumerate(siteswaps):
        print(idx+1, "/", len(siteswaps))
        max_balls = int(sum(int(char) for char in ss) / len(ss))
        res = execute(evaluate = False, tracking_system = tracking_systems[0], color_range = color_range, max_balls = max_balls, tracking_preprocessing = False, max_cuadrant_misses = 0.35, ss_test_numbers = 5, ss=ss, save_data = 2)
        table.add_row(res)
    print(table) """

            
            