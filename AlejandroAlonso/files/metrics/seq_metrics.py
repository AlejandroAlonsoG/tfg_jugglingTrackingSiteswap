from polyleven import levenshtein
from prediction.ss_prediction import get_min_period, prediction, get_full_ss_string

def seq_metrics(ss, gtSource, tSource, name):
    gt = ''.join(str(x) for x in gtSource)
    t = ''.join(str(x) for x in tSource)
    edit_distance = levenshtein(gt, t)
    ss_string = get_full_ss_string(tSource)
    pred = prediction(tSource)
    is_present = 'True' if ss in ss_string else 'False'
    try:
        presence = ss_string.count(ss)/(len(ss_string)/len(ss))
        period = 'True' if len(ss) == get_min_period(ss_string, len(ss_string)//2, 10) else 'False'
    except:
        presence = 'None'
        period = 'False'
    works = 'True' if ss == pred else 'False'

    format = "{:<10} {:<15} {:<12} {:<20} {:<10} {:<10}"

    

    return format.format(name,edit_distance,is_present,presence,period,works)

if __name__ == "__main__":
    gt = [1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3]
    t1 = [1,2,3,2,1,3,1,2,3,2,1,3,1,2,3,2,1,3]
    t2 = [1,2,3,4,2,3,4,2,3,4,2,3,4,2,3,4,2,3]
    format = "{:<10} {:<15} {:<12} {:<20} {:<10} {:<10}"
    print(format.format("name","edit_distance", "is_present", "presence", "period", "works"))
    print(seq_metrics('3',gt, t1, 't1'))
    print(seq_metrics('3',gt, t2, 't2'))