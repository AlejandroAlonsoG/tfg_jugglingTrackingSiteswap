from tracking.preprocessing.color_extractor import color_extractor
from tracking.color_tracking_max_balls import color_tracking_max_balls
from tracking.color_tracking_v0 import color_tracking
from tracking.bg_substraction_tracking_max_balls import bg_substraction_tracking_max_balls
from tracking.bg_substraction_tracking import bg_substraction_tracking
from prediction.seq_extractor import seq_extraction, seq_extraction_cuadrants
from prediction.ss_prediction import prediction, get_full_ss_string
from prediction.ss_prediction import get_full_ss_string
from prediction.seq_preprocessing import point_extractor
from prettytable import PrettyTable
from tracking.data_saver_files.mot16_utils import load_data 

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

  motp = summary['motp'][0]
  mota = summary['mota'][0]

  return motp, mota

def get_evaluation(tracking_path, gt_path, throw_seq, ss):
    motp, mota = motMetricsEnhancedCalculator(gt_path, tracking_path)
    ss_string = get_full_ss_string(throw_seq)
    try:
        presence = ss_string.count(ss)/(len(ss_string)/len(ss))
    except:
        presence = -1

    return motp, mota, presence

def execute(evaluate = False, tracking_system = "", color_range = None, max_balls = None, tracking_preprocessing = False, max_cuadrant_misses = 20, ss_test_numbers = 5, ss=None, save_data = -1):
            source_path = dataset_dir + video_file_format.format(ss)
            # Module "Detection-tracking"

            # Preprocessing #
            if tracking_preprocessing:
                color_range = color_extractor(source_path)

            # Tracking #
            if tracking_system == "ColorTrackingMaxBalls":
                if max_balls == None or color_range == None:
                      raise Exception("ColorTrackingMaxBalls - Wrong parameters")
                ids = color_tracking_max_balls(source_path, color_range, max_balls = max_balls,visualize=False, save_data=save_data)
            elif tracking_system == "ColorTrackingV0":
                if color_range == None:
                     raise Exception("ColorTrackingV0 - Wrong parameters")
                ids = color_tracking(source_path, color_range, visualize=False, save_data=save_data)
            elif tracking_system == "BgSubstractionMaxBalls":
                if max_balls == None:
                    raise Exception("BgSubstractionMaxBalls - Wrong parameters")
                ids = bg_substraction_tracking_max_balls(source_path, max_balls=max_balls, visualize=False, save_data=save_data)
            elif tracking_system == "BgSubstraction":
                ids = bg_substraction_tracking(source_path, visualize=False, save_data=save_data)
            else:
                raise Exception("Wrong tracking system")

            # Module "SS Extraction"

            # Seq_extraction
            point = point_extractor(source_path)
            
            ids2 = load_data(tracking_dir+tracking_file_format.format(ss, tracking_system))
            throw_seq1_cuadrants, num_misses = seq_extraction_cuadrants(ids, point, 0,0)
            throw_seq2_cuadrants, num_misses = seq_extraction_cuadrants(ids2, point, 0,0)
            #if num_misses > max_cuadrant_misses:
            throw_seq_1= seq_extraction(ids)
            throw_seq_2= seq_extraction(ids2)
            
            # SS extraction
            ss_pred_traj_1 = prediction(throw_seq_1, test_numbers=ss_test_numbers)
            ss_pred_traj_2 = prediction(throw_seq_2, test_numbers=ss_test_numbers)
            ss_pred_cuadrants_1 = prediction(throw_seq1_cuadrants, test_numbers=ss_test_numbers)
            ss_pred_cuadrants_2 = prediction(throw_seq2_cuadrants, test_numbers=ss_test_numbers)


            # Evaluation and return
            works_traj_1 = eq_ss(ss, ss_pred_traj_1)
            works_traj_2 = eq_ss(ss, ss_pred_traj_2)
            works_cuadrants_1 = eq_ss(ss, ss_pred_cuadrants_1)
            works_cuadrants_2 = eq_ss(ss, ss_pred_cuadrants_2)

            if not evaluate:
                return ss, works_traj_1, works_traj_2, works_cuadrants_1, works_cuadrants_2, works_traj_1 or works_traj_2 or works_cuadrants_1 or works_cuadrants_2
            else:
                return None

if __name__ == "__main__":
    siteswaps = ['1', '40', '31', '4', '330', '3', '423', '441', '531', '51', '633', '5551', '525', '534', '66611', '561', '75314', '5', '645', '744', '91', '6', '7']
    tracking_systems = ['ColorTrackingMaxBalls', 'ColorTrackingV0', 'BgSubstractionMaxBalls', 'BgSubstraction']
    color_range = 168,140,69,175,255,198
    #color_range = 0,50,0,255,255,255
    table = PrettyTable()
    table.field_names = ["ss", "works_traj_1", "works_traj_2", "works_cuadrants_1", "works_cuadrants_2", "Works any"]
    for idx, ss in enumerate(siteswaps):
        print(idx+1, "/", len(siteswaps))
        max_balls = int(sum(int(char) for char in ss) / len(ss))
        res = execute(evaluate = False, tracking_system = tracking_systems[0], color_range = color_range, max_balls = max_balls, tracking_preprocessing = False, max_cuadrant_misses = 8, ss_test_numbers = 5, ss=ss, save_data = 2)
        table.add_row(res)
    print(table)

            
            