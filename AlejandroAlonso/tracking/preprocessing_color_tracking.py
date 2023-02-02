from preprocessing.color_extractor import color_extractor
from color_tracking import color_tracking
color_range = 35,30,150,185,120,255 #RED_Alex
source_path = '/home/alex/tfg_jugglingTrackingSiteswap/dataset/ss5_red_AlejandroAlonso.mp4'

color_range = color_extractor(source_path, size=1)
print(color_range)
color_tracking(source_path, color_range, visualize=False)