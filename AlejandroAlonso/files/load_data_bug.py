from tracking.data_saver_files.mot16_utils import *

save_dir='/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/mot16/Tracking/3_ColorTrackingMaxBalls.txt'

ids = load_data(save_dir)

file = file_initializer("test", "3", "Tracking")
for i in range(len(ids[1]['x'])):
    for id in range(1,len(ids)+1):
        try:
            tmp = ids[id]['x'][i]
            file_writer(file, i+1, id, (ids[id]['x'][i],ids[id]['y'][i]))
        except:
            pass   

file_saver(file)