from tracking.color_tracking_max_balls import color_tracking_max_balls



color_range = 35,30,150,185,120,255 #RED_Alex
#source_path = '/home/alex/tfg_jugglingTrackingSiteswap/dataset/ss5_red_AlejandroAlonso.mp4'
source_path = '/home/alex/tfg_jugglingTrackingSiteswap/dataset/tests/short.mp4'

#color_range = color_extractor(source_path)
print(color_range)
color_tracking_max_balls(source_path, color_range, visualize=True, save_data=2)
#color_then_bgSubstraction_tracking(source_path, color_range, visualize=False)