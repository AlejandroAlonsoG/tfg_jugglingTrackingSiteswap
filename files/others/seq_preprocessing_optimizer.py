import concurrent.futures
from prediction.seq_extractor import seq_extraction_cuadrants
from prediction.ss_prediction import prediction
from prediction.seq_preprocessing import point_extractor
from tracking.data_saver_files.mot16_utils import load_data 
# CONSTANTS
gt_dir = './AlejandroAlonso/results/mot16/GroundTruth/'
tracking_dir = './AlejandroAlonso/results/mot16/Tracking/'
dataset_dir = './dataset/tanda2/'
#dataset_dir = './dataset/jugglingLab/'
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

def test(min_area):
    print("Starting: ", min_area)
    siteswaps = ['1', '40', '31', '4', '330', '3', '423', '441', '531', '51', '633', '5551', '525', '534', '66611', '561', '75314', '5', '645', '744', '91', '6', '7']
    count =0
    for ss in siteswaps:
        source_path = dataset_dir + video_file_format.format(ss)
        ids = load_data(tracking_dir+tracking_file_format.format(ss, 'ColorTrackingMaxBalls'))
        point = point_extractor(source_path, min_contour_area=min_area)
        seq = seq_extraction_cuadrants(ids, point, 0, 0)
        pred = prediction(seq[0])
        if eq_ss(pred, ss):
            count += 1
    
    print("Finished: ", min_area, count)
    return min_area, count

def main():
    min_areas = range(1750,2751,50) #1750 - 2250 hacen 12

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Para cada valor de 'param' creamos un objeto Future que ejecuta la función 'test'
        futures = {executor.submit(test, min_area): (min_area) for min_area in min_areas}

        # Esperamos a que todas las ejecuciones de la función 'test' terminen
        concurrent.futures.wait(futures)
        with open("./AlejandroAlonso/results/res_seq_preprocessing_optimizer.txt", "w") as f:
            for future in futures:
                f.write(f'{future.result()}\n')

if __name__ == '__main__':
    main()
