import sys, cv2
sys.path.insert(0, '../excel_utils')
import excel_utils as eu
import numpy as np

#source_path='/home/alex/tfg_jugglingTrackingSiteswap/dataset/ss5_red_Unknown.mp4' # Url of source video
#path_book='/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/excels/tracking_short_denoise.xlsx'
#path_book='/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/excels/tracking_short_StephenMeschke.xlsx' 

#source_path='/home/alex/tfg_jugglingTrackingSiteswap/dataset/tests/short.mp4' # Url of source video
path_book='/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/excels/tracking_ss5_StephenMeschke.xlsx'

source_path='/home/alex/tfg_jugglingTrackingSiteswap/dataset/ss5_red_AlejandroAlonso.mp4' # Url of source video
#path_book='/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/excels/tracking_5_AlejandroAlonso_red.xlsx'

output_path='/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/videos/'

visualize=True
square_len=50

# Saca el color en hsv para poder hacerlos distintos y luego lo pasa a bgr
def getDistinctColors(id, num_balls):
    h = (int(360/num_balls * id))
    r, g, b = cv2.cvtColor(np.uint8([[[h / 2, 255, 255]]]), cv2.COLOR_HSV2BGR)[0][0]
    return (int(r), int(g), int(b))

data,num_balls = eu.load_data(path_book)
cv2.namedWindow('img', cv2.WINDOW_NORMAL)

cap = cv2.VideoCapture(source_path)
_, img = cap.read()
out_name=(source_path.split('/')[-1]).split('.')[0]+'_tracking.mp4'
w,h = img.shape[:2]
out = cv2.VideoWriter(output_path+out_name, cv2.VideoWriter_fourcc(*"mp4v"), 30, (h,w))
num_frame=0
ret=True

colors = []
for i in range(num_balls):
    colors.append(getDistinctColors(i, num_balls))
colors_reorder = [colors[i] for i in range(0, num_balls, 3)] + [colors[i] for i in range(1, num_balls, 3)] + [colors[i] for i in range(2, num_balls, 3)]

while(cap.isOpened()):
    if ret==True:
        for i in range(num_balls):
            try: # Las coordenadas de la bola para ese frame puede ser None y salta excepcion con la división entera, además el último índice tampoco entra
                coords_x, coords_y = data[i][num_frame]
                start_point = (coords_x-square_len//2, coords_y-square_len//2)
                end_point = (coords_x+square_len//2, coords_y+square_len//2)
                #cv2.circle(img, coords, 20, (0, 0, 255), -1)
                cv2.rectangle(img, start_point, end_point, colors_reorder[i], 4)
                org = (coords_x+square_len//2+2, coords_y-square_len//2+2)
                cv2.putText(img, str(i+1), org, cv2.FONT_HERSHEY_SIMPLEX, 2, colors_reorder[i], 4)
            except: pass
        num_frame +=1
        out.write(img)
        if visualize:
            cv2.imshow('img', img)
            cv2.waitKey(0)
    else:
        break
    ret, img = cap.read()

print(num_frame)
cap.release()
out.release()
cv2.destroyAllWindows()