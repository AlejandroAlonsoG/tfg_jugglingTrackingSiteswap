from polyleven import levenshtein
from prediction.ss_prediction import get_min_period, prediction, get_full_ss_string
from tracking.color_tracking_max_balls import color_tracking_max_balls
from tracking.color_tracking_v0 import color_tracking
from prediction.seq_extractor import seq_extraction_cuadrants
from prediction.ss_prediction import prediction
from prediction.seq_preprocessing import bg_substraction_tracking
from tracking.data_saver_files.mot16_utils import load_data
from prettytable import PrettyTable


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
 
    sources = ['/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/mot16/GroundTruth/{}_manual.txt',
               '/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/mot16/Tracking/{}_ColorTrackingMaxBalls.txt']
    sources = ['/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/mot16/Tracking/{}_ColorTrackingMaxBalls.txt']
    # ss, num_balls, [GT]
    siteswaps = [
        ('1',1, [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]), \
        ('3',3, [0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1,2]), \
        ('423',3, [0,1,0,2,0,1,0,2,0,1,0,2,0,1,0,2,0,1,0,2,0,1,0,2,0,1,0,2,0,1,0,2,0,1,0,2,0,1,0,2]), \
        ('441',3, [0,1,2,2,0,1,1,2,0,0,1,2,2,0,1,1,2,0,0,1,2,2,0,1,1,2,0,0,1,2,2,0,1,1,2,0,0,1,2,2,0,1,1,2,0,0,1,2,2,0,1,1,2,0,0,1,2,2,0,1,1,2,0]), \
        ('5',5, [0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0])
    ]
    # Configuration
    color_range = 35,30,150,185,120,255


    # Dos formas, desde GT, y desde tracking (mejor de los que tenga)


    # Sacar para cada forma y para cada ss:
        # Distancia edición secuencia respecto GT
        # Num misses en caso de seq2
        # Funcionamiento después con la función del ss:
            # Resultado obtenido
            # Distancia edición del ss respecto al GT
            # Si el ss GT está al menos presente en el resultado, y en caso afirmativo su %
            # Si el periodo del resultado es el del GT
            # Si funciona perfecto
    for source in sources:
        print(source)
        table = PrettyTable()
        table.field_names = ["ss", "edit_distance_seq", "num_misses", "res", "edit_distance_ss", "is_present", "percentaje", "same_period", "works"]
        for ss, max_balls, gt in siteswaps: 
            source_path = source.format(ss)
            # Tracking
            ids = load_data(source_path)
            # Seq prep
            point = bg_substraction_tracking('/home/alex/tfg_jugglingTrackingSiteswap/dataset/ss{}_red_AlejandroAlonso.mp4'.format(ss),convergence_threshold=0)
            print(point)
            # Seq
            throw_seq, num_misses = seq_extraction_cuadrants(ids, point, 0,0)
            # SS
            res_seq = seq_metrics(ss, throw_seq)

            table.add_row([ss, str(levenshtein(''.join(str(x) for x in gt), ''.join(str(x) for x in throw_seq))),
                                                                num_misses, str(res_seq[0]), str(res_seq[1]),str(res_seq[2]),str(res_seq[3]),str(res_seq[4]),str(res_seq[5])])

        print(table)



