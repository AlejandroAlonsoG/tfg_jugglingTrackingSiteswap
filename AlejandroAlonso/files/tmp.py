from tracking.color_tracking_max_balls import color_tracking_max_balls
from prediction.seq_extractor_tmp import seq_extraction, seq_extraction_cuadrants
from prediction.ss_prediction_tmp import prediction
from prediction.seq_preprocessing import point_extractor
from tracking.data_saver_files.mot16_utils import load_data 
from prediction.seq_extractor import seq_extraction as seq_extraction2
from prediction.ss_prediction import prediction as prediction2


# Configuration
source_path = '/home/alex/tfg_jugglingTrackingSiteswap/dataset/instagram/ss9_rohanjuggler.mp4'
color_range = 95, 85, 48, 117, 255, 190
ss = '9'
max_balls = 9
# Tracking
ids1 = color_tracking_max_balls(source_path, color_range, max_balls=max_balls, visualize=True, save_data=2)
ids2 = load_data('/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/mot16/Tracking/'+ss+'_ColorTrackingMaxBalls.txt')

# Seq_extraction
point = point_extractor(source_path)
try:
    throw_seq_c_1, num_misses = seq_extraction_cuadrants(ids1, point, 0,0)
    throw_seq_c_2, num_misses = seq_extraction_cuadrants(ids2, point, 0,0)
except:
    throw_seq_c_1 = []
    throw_seq_c_2 = []
throw_seq_1 = seq_extraction(ids1)
throw_seq_2 = seq_extraction2(ids2)
# SS extraction
pred_1_1, full_ss = prediction(throw_seq_1, num_balls=max_balls, test_numbers=5)
pred_1_2, full_ss = prediction(throw_seq_2, num_balls=max_balls, test_numbers=5)
pred_1_c_1, full_ss = prediction(throw_seq_c_1, num_balls=max_balls, test_numbers=5)
pred_1_c_1, full_ss = prediction(throw_seq_c_2, num_balls=max_balls, test_numbers=5)
pred_2_1 = prediction2(throw_seq_1, test_numbers=5)
pred_2_2 = prediction2(throw_seq_2, test_numbers=5)
pred_2_c_1 = prediction2(throw_seq_c_1, test_numbers=5)
pred_2_c_1 = prediction2(throw_seq_c_2, test_numbers=5)

print("{}->{}".format(ss,pred_1_1))
print("{}->{}".format(ss,pred_1_2))
print("{}->{}".format(ss,pred_1_c_1))
print("{}->{}".format(ss,pred_1_c_1))
print("{}->{}".format(ss,pred_2_1))
print("{}->{}".format(ss,pred_2_2))
print("{}->{}".format(ss,pred_2_c_1))
print("{}->{}".format(ss,pred_2_c_1))
""" 
print("Orden de los lanzamientos: ", throw_seq)
print("Siteswap obtenido2: ", ss2)
print("Siteswap obtenido3: ", ss3)
print("Siteswap obtenido4: ", ss4)
print("Siteswap obtenido5: ", ss5)
print("Siteswap obtenido10: ", ss10) """
