from polyleven import levenshtein
from prediction.ss_prediction import get_min_period, prediction, get_full_ss_string
from tracking.color_tracking_max_balls import color_tracking_max_balls
from tracking.color_tracking_v0 import color_tracking
from prediction.seq_extractor import seq_extraction
from prediction.ss_prediction import prediction


def seq_metrics(ss, tSource):
    pred = prediction(tSource)
    edit_distance = levenshtein(ss, pred)
    ss_string = get_full_ss_string(tSource)
    is_present = 'True' if ss in ss_string else 'False'
    try:
        presence = ss_string.count(ss)/(len(ss_string)/len(ss))
        period = 'True' if len(ss) == len(pred) else 'False'
    except:
        presence = 'None'
        period = 'False'
    works = 'True' if ss == pred else 'False'

    return pred, edit_distance,is_present,presence,period,works

if __name__ == "__main__":
 
    siteswaps = [
        ('1',1, [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]), \
        ('3',3, [0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1,2]), \
        ('423',3, [0,1,0,2,0,1,0,2,0,1,0,2,0,1,0,2,0,1,0,2,0,1,0,2,0,1,0,2,0,1,0,2,0,1,0,2,0,1,0,2]), \
        ('441',3, [0,1,2,2,0,1,1,2,0,0,1,2,2,0,1,1,2,0,0,1,2,2,0,1,1,2,0,0,1,2,2,0,1,1,2,0,0,1,2,2,0,1,1,2,0,0,1,2,2,0,1,1,2,0,0,1,2,2,0,1,1,2,0]), \
        ('5',5, [0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0])
    ]
    # Configuration
    color_range = 35,30,150,185,120,255

    for ss, max_balls, gt in siteswaps:
        source_path = '/home/alex/tfg_jugglingTrackingSiteswap/dataset/ss'+ss+'_red_AlejandroAlonso.mp4'
        # Tracking
        ids_color = color_tracking(source_path, color_range, visualize=False)
        ids_max_balls = color_tracking_max_balls(source_path, color_range, max_balls=max_balls, visualize=False)
        # Seq
        throw_seq_color = seq_extraction(ids_color)
        throw_seq_max_balls = seq_extraction(ids_max_balls)
        # SS
        res_seq_color = seq_metrics(ss, throw_seq_color)
        res_seq_max_balls = seq_metrics(ss, throw_seq_max_balls)
        print("ss"+ss)
        print("seq_extractor")
        print("system\tedit_distance")
        print("Color\t"+str(levenshtein(''.join(str(x) for x in gt), ''.join(str(x) for x in throw_seq_color))))
        print("Max_balls\t"+str(levenshtein(''.join(str(x) for x in gt), ''.join(str(x) for x in throw_seq_max_balls))))
        print("ss_extractor")
        print("system\tres\tedit_distance\tis_present\tpresence\tperiod\tworks")
        print("Color\t{}\t{}\t{}\t{}\t{}\t{}".format(str(res_seq_color[0]),str(res_seq_color[1]),str(res_seq_color[2]),str(res_seq_color[3]),str(res_seq_color[4]),str(res_seq_color[5])))
        print("Max_balls\t{}\t{}\t{}\t{}\t{}\t{}".format(str(res_seq_max_balls[0]),str(res_seq_max_balls[1]),str(res_seq_max_balls[2]),str(res_seq_max_balls[3]),str(res_seq_max_balls[4]),str(res_seq_max_balls[5])))



