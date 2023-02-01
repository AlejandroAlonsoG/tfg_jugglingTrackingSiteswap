from preprocessing.color_extractor import color_extractor
from color_tracking import color_tracking
color_range = 35,30,150,185,120,255 #RED_Alex
source_path = '/home/alex/tfg_jugglingTrackingSiteswap/dataset/ss3_red_AlejandroAlonso.mp4'

""" 0.9 25 35 25 28
    0.8 29 30 29 17
    0.7 24 23 24 19
    0.6 23 25 23 22
    0.5 25 28 25 22
    0.4 19 14 19 13
    0.3 10 12 10 8
    0.2 12 11 12 10
    0.1 90 95 90 94
    """
""" for umbral in [x * 0.1 for x in range(9, 0, -1)]:
    color_range = color_extractor(source_path, index_umbral=umbral)
    print("Obtenido color_range:", color_range)
    ret = color_tracking(source_path, color_range)
    print(umbral, color_range, ret) """

color_range = color_extractor(source_path, index_umbral=0.7)
print("Obtenido color_range:", color_range)
ret = color_tracking(source_path, color_range)
print(ret)

