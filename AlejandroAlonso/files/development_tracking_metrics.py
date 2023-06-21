from tracking.preprocessing.color_extractor import color_extractor
from tracking.color_tracking_max_balls import color_tracking_max_balls
from tracking.color_tracking_v0 import color_tracking as color_trackingV0
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

def format_motp(motp):
  return '{:.2%}'.format(1 - motp)

def motMetricsEnhancedCalculator(ss, gtSource, tSource, decimal_round):
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

  """ summary = mh.compute(acc, metrics=['num_frames', 'idf1', 'idp', 'idr', \
                                     'recall', 'precision', 'num_objects', \
                                     'mostly_tracked', 'partially_tracked', \
                                     'mostly_lost', 'num_false_positives', \
                                     'num_misses', 'num_switches', \
                                     'num_fragmentations', 'mota', 'motp' \
                                    ], \
                      name='acc') """
  
  summary = mh.compute(acc, metrics=['num_fragmentations', 'num_misses', 'num_false_positives', 'num_switches', \
                                     'num_unique_objects', 'mostly_lost', 'partially_tracked', 'mostly_tracked', \
                                     'recall', 'precision', 'mota', 'motp'
                                    ])
  
  num_fragmentations = summary['num_fragmentations'][0]
  num_misses = summary['num_misses'][0]
  num_false_positives = summary['num_false_positives'][0]
  num_switches = summary['num_switches'][0]
  num_unique_objects = summary['num_unique_objects'][0]
  mostly_lost = summary['mostly_lost'][0]
  mostly_tracked = summary['mostly_tracked'][0]
  partially_tracked = summary['partially_tracked'][0]
  recall = summary['recall'][0]
  precision = summary['precision'][0]
  motp = (1 - summary['motp'][0])
  mota = summary['mota'][0]

  return ss, num_fragmentations,num_misses,num_false_positives,num_switches,num_unique_objects,mostly_lost,partially_tracked,mostly_tracked,round(recall,decimal_round),round(precision,decimal_round),round(mota,decimal_round),round(motp,decimal_round)

def execute(tracking_system = "", color_range = None, max_balls = None, tracking_preprocessing = False, decimal_round=3, ss=None, save_data = -1):
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
                color_trackingV0(source_path, color_range, visualize=False, save_data=save_data)
            elif tracking_system == "BgSubstractionMaxBalls":
                if max_balls == None:
                    raise Exception("BgSubstractionMaxBalls - Wrong parameters")
                bg_substraction_tracking_max_balls(source_path, max_balls=max_balls, visualize=False, save_data=save_data)
            elif tracking_system == "BgSubstractionV0":
                bg_substraction_tracking(source_path, visualize=False, save_data=save_data)
            else:
                raise Exception("Wrong tracking system")

            tracking_file_path = tracking_dir+tracking_file_format.format(ss, tracking_system)
            gt_file_path = gt_dir+gt_file_format.format(ss)
            print("Terminado: ", ss)
            return motMetricsEnhancedCalculator(ss, gt_file_path, tracking_file_path, decimal_round)


if __name__ == "__main__":
    #siteswaps = ['1', '40', '31', '4', '330', '3', '423', '441', '531', '51', '633', '5551', '525', '534', '66611', '561', '75314', '5', '645', '744', '91', '6']
    siteswaps = ['1', '3', '423', '441', '5']
    tracking_systems = ['ColorTrackingMaxBalls', 'ColorTrackingV0', 'BgSubstractionMaxBalls', 'BgSubstractionV0']
    color_range = 168,140,69,175,255,198
    #color_range = 0, 50, 0, 255, 255, 255
    table = PrettyTable()
    table.field_names = ["ss", "Track perdido", "Detec. Perdidas", "Detec. Ruido", "ID Swap", "Num Bolas", "<20\%", "20-80\%", ">80\%", "Recall", "Precision", "MOTA", "MOTP"]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Para cada valor de 'param' creamos un objeto Future que ejecuta la función 'test'
        futures = {executor.submit(execute, tracking_systems[2], color_range, int(sum(int(char) for char in ss) / len(ss)), False, 3, ss, 2): (ss) for ss in siteswaps}

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

            
            