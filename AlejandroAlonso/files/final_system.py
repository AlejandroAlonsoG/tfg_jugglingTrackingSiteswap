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
import yaml

def eq_ss(str1, str2):
    if len(str1) != len(str2):
        return False
    else:
        str1_str1 = str1 + str1
        return str2 in str1_str1

def motMetricsEnhancedCalculator(gtSource, tSource):
  # import required packages
  import motmetrics as mm
  import numpy as np
  
  # load ground truth
  gt = np.loadtxt(gtSource, delimiter=',')

  # load tracking output
  t = np.loadtxt(tSource, delimiter=',')

  # Create an accumulator that will be updated during each frame
  acc = mm.MOTAccumulator(auto_id=True)

  # Max frame number maybe different for gt and t files
  for frame in range(int(gt[:,0].max())):
    frame += 1 # detection and frame numbers begin at 1

    # select id, x, y, width, height for current frame
    # required format for distance calculation is X, Y, Width, Height \
    # We already have this format
    gt_dets = gt[gt[:,0]==frame,1:6] # select all detections in gt
    t_dets = t[t[:,0]==frame,1:6] # select all detections in t

    C = mm.distances.iou_matrix(gt_dets[:,1:], t_dets[:,1:], \
                                max_iou=0.8) # format: gt, t

    # Call update once for per frame.
    # format: gt object ids, t object ids, distance
    acc.update(gt_dets[:,0].astype('int').tolist(), \
              t_dets[:,0].astype('int').tolist(), C)

  mh = mm.metrics.create()

  summary = mh.compute(acc, metrics=['mota', 'motp'])

  motp = (1 - summary['motp'][0])
  mota = summary['mota'][0]

  return motp, mota

def get_evaluation(tracking_path, gt_path, full_ss, ss):
    motp, mota = motMetricsEnhancedCalculator(gt_path, tracking_path)
    try:
        presence = full_ss.count(ss)/(len(full_ss)/len(ss))
    except:
        presence = -1

    return motp, mota, presence

def execute(evaluate = False, tracking_system = "", color_range = None, max_balls = None, tracking_preprocessing = False, max_cuadrant_misses = 0.35, ss_test_numbers = 5, max_perido_threshold=1.5, decimal_round=3, ss=None, save_data = -1):
            source_path = dataset_dir + video_file_format.format(ss)
            # Module "Detection-tracking"

            # Preprocessing #
            if tracking_preprocessing:
                color_range = color_extractor(source_path)

            # Tracking #
            if tracking_system == "ColorTrackingMaxBalls":
                if max_balls == None or color_range == None:
                      raise Exception("ColorTrackingMaxBalls - Wrong parameters")
                color_tracking_max_balls(source_path, color_range, max_balls = max_balls,visualize=False, save_data=save_data)
            elif tracking_system == "ColorTrackingV0":
                if color_range == None:
                     raise Exception("ColorTrackingV0 - Wrong parameters")
                color_tracking(source_path, color_range, visualize=False, save_data=save_data)
            elif tracking_system == "BgSubstractionMaxBalls":
                if max_balls == None:
                    raise Exception("BgSubstractionMaxBalls - Wrong parameters")
                bg_substraction_tracking_max_balls(source_path, max_balls=max_balls, visualize=False, save_data=save_data)
            elif tracking_system == "BgSubstractionV0":
                bg_substraction_tracking(source_path, visualize=False, save_data=save_data)
            else:
                raise Exception("Wrong tracking system")

            # Module "SS Extraction"

            # Seq_extraction
            point = point_extractor(source_path)
            
            ids = load_data(tracking_dir+tracking_file_format.format(ss, tracking_system))
            system_used = 'Cuadrants'
            throw_seq, num_misses = seq_extraction_cuadrants(ids, point, 0,0)
            if num_misses > max_cuadrant_misses:
                system_used = 'Coords as a function'
                throw_seq = seq_extraction(ids)
            num_misses = round(num_misses, decimal_round)
            
            # SS extraction
            ss_pred, full_ss = prediction(throw_seq, num_balls=max_balls, test_numbers=ss_test_numbers)
            if system_used=='Cuadrants' and (ss_pred == 'NotFound' or len(ss_pred) > max_balls*max_perido_threshold):
                throw_seq = seq_extraction(ids)
                ss_pred, full_ss = prediction(throw_seq, num_balls=max_balls, test_numbers=ss_test_numbers)
                system_used = 'Coords as a function'
                if len(ss_pred) > max_balls*max_perido_threshold:
                    ss_pred = 'NotFound'
            #ss_pred_cuadrants = prediction(throw_seq_cuadrants, test_numbers=ss_test_numbers)

            # Evaluation and return
            works = eq_ss(ss, ss_pred)
            #works_cuadrants = eq_ss(ss, ss_pred_cuadrants)

            print("Finished: ", ss)
            if not evaluate:
                if system_used == 'Cuadrants':
                    return ss, '---', '---', '---', ss_pred, system_used, num_misses, works
                else:
                    return ss, '---', '---', '---', ss_pred, system_used, '---' , works
            else:
                if save_data == -1:
                    raise Exception("evaluate and save_data = -1")
                tracking_file_path = tracking_dir+tracking_file_format.format(ss, tracking_system)
                gt_file_path = gt_dir+gt_file_format.format(ss)
                motp, mota, presence = get_evaluation(tracking_file_path, gt_file_path, full_ss, ss)
                motp = round(motp, decimal_round)
                mota = round(mota, decimal_round)
                presence = round(presence, decimal_round)
                if system_used == 'Cuadrants':
                    return ss, motp, mota, presence, ss_pred, system_used, num_misses, works
                else:
                    return ss, motp, mota, presence, ss_pred, system_used, '---', works


if __name__ == "__main__":
    with open('AlejandroAlonso/files/config.yml', 'r') as f:
        config = yaml.safe_load(f)

    # CONSTANTS
    global gt_dir 
    global tracking_dir
    global dataset_dir 
    global video_file_format 
    global gt_file_format
    global tracking_file_format
    gt_dir = config['gt_dir']
    tracking_dir = config['tracking_dir']
    dataset_dir = config['dataset_dir']
    video_file_format = config['video_file_format']
    gt_file_format = config['gt_file_format']
    tracking_file_format= config['tracking_file_format']

    # PARAMETERS
    siteswaps = config['siteswaps']
    tracking_systems = config['tracking_systems']
    color_range = [int(num) for num in config['color_range'].split(',')]
    evaluate = config['evaluate']
    tracking_preprocessing = config['tracking_preprocessing']
    max_cuadrant_misses = config['max_cuadrant_misses']
    ss_test_numbers = config['ss_test_numbers']
    max_perido_threshold = config['max_perido_threshold']
    decimal_round = config['decimal_round']
    save_data = config['save_data']

    table = PrettyTable()
    table.field_names = config['table_field_names']

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Para cada valor de 'param' creamos un objeto Future que ejecuta la función 'test'
        futures = {executor.submit(execute, evaluate, tracking_systems[0], color_range, int(sum(int(char) for char in ss) / len(ss)), tracking_preprocessing, max_cuadrant_misses, ss_test_numbers, max_perido_threshold, decimal_round, ss, save_data): (ss) for ss in siteswaps}

        # Esperamos a que todas las ejecuciones de la función 'test' terminen
        concurrent.futures.wait(futures)
    
    for future in futures:
        print(future.result())
        table.add_row(future.result())
    print(table)

    """ for idx, ss in enumerate(siteswaps):
        print(idx+1, "/", len(siteswaps))
        max_balls = int(sum(int(char) for char in ss) / len(ss))
        res = execute(evaluate = False, tracking_system = tracking_systems[0], color_range = color_range, max_balls = max_balls, tracking_preprocessing = False, max_cuadrant_misses = 0.35, ss_test_numbers = 5, ss=ss, save_data = 2)
        table.add_row(res)
    print(table) """

            
            