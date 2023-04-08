# import required packages
import motmetrics as mm
import numpy as np
from prettytable import PrettyTable

def format_motp(motp):
  return '{:.2%}'.format(1 - motp)

def motMetricsEnhancedCalculator(ss, gtSource, tSource):
  
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
                                    ], \
                      name=ss)
  

  strsummary = mm.io.render_summary(
      summary,
      #formatters={'mota' : '{:.2%}'.format, 'motp' : format_motp,'recall' : '{:.2%}'.format,'precision' : '{:.2%}'.format},
      namemap={'num_fragmentations' : 'T. Perdido', 'num_misses': 'D. Perdidas', 'num_false_positives': 'D. Ruido', \
               'num_switches' : 'ID swap', 'num_unique_objects': 'nBalls', 'mostly_lost' : '<20%', \
               'mostly_tracked' : '>80%', 'partially_tracked': '20%80%', 'recall': 'Recall', \
               'precision': 'Precision', 'mota': 'MOTA', 'motp' : 'MOTP',  \
              }
  )

  return strsummary.split("\n")[-1]

if __name__ == "__main__":
    siteswaps = ['1', '3', '423', '441', '5']
    table = PrettyTable()
    table.field_names = ['T. Perdido', 'D. Perdidas', 'D. Ruido', 'ID swap', 'nBalls', '<20%', \
            '>80%', '20%80%', 'Recall', 'Precision', 'MOTA', 'MOTP']
    for ss in siteswaps:
        ret = motMetricsEnhancedCalculator(ss,'/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/mot16/GroundTruth/'+ss+'_manual.txt', '/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/mot16/Tracking/'+ss+'_ColorTracking.txt')
        table.add_row()
    print(table)
