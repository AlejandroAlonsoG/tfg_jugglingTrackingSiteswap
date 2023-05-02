import sys, cv2
sys.path.insert(0, '../excel_utils')
import tracking.data_saver_files.excel_utils as eu
import tracking.data_saver_files.mot16_utils as mu
import numpy as np
from PIL import Image

save_dir='/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/'
dataset_dir='/home/alex/tfg_jugglingTrackingSiteswap/dataset/tanda2/'
#dataset_dir='/home/alex/tfg_jugglingTrackingSiteswap/dataset/jugglingLab/'
output_path='/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/videos/'

#path_book = '/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/excels/tracking_short_ColorTracking.xlsx'
#path_book = '/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/excels/tracking_short_manual.xlsx'
#path_book = '/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/excels/tracking_ss3_red_AlejandroAlonso_ColorTracking.xlsx'
#path_book = '/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/excels/tracking_ss5_red_AlejandroAlonso_ColorTracking.xlsx'
#path_book = '/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/excels/50.xlsx'

#path_book = '/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/mot16/GroundTruth/3_manual.txt'
#path_book1 = '/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/excels/tracking_ss3_red_AlejandroAlonso_ColorTracking.xlsx'

#source_path='/home/alex/tfg_jugglingTrackingSiteswap/dataset/tests/short.mp4' # Url of source video
#source_path='/home/alex/tfg_jugglingTrackingSiteswap/dataset/ss3_red_AlejandroAlonso.mp4' # Url of source video
#source_path='/home/alex/tfg_jugglingTrackingSiteswap/dataset/ss5_red_AlejandroAlonso.mp4' # Url of source video



# Saca el color en hsv para poder hacerlos distintos y luego lo pasa a bgr
def getDistinctColors(id, num_balls):
    h = (int(360/num_balls * id))
    r, g, b = cv2.cvtColor(np.uint8([[[h / 2, 255, 255]]]), cv2.COLOR_HSV2BGR)[0][0]
    return (int(r), int(g), int(b))

def tracking_visualizer(ss, system, save_dir, dataset_dir, output_path, visualize=True,\
                        square_len=50, video_source = 'red_AlejandroAlonso', point=None, trayectory_limit = 10, file_mode=2):
    
    if file_mode==1:
        save_dir+='excels/'
    else:
        save_dir+='mot16/'
    if system == 'manual':
        save_dir+='GroundTruth/'
    else:
        save_dir+='Tracking/'
    f'{save_dir}{ss}_{system}.txt'
    path_book = f'{save_dir}{ss}_{system}'
    if file_mode==1:
        path_book+='.xlsx'
    else:
        path_book+='.txt'

    source_path= f'{dataset_dir}ss{ss}_{video_source}.mp4'
    if file_mode==1:
        data,num_balls = eu.load_data(path_book)
    else:
        data,num_balls = mu.load_data_visualizer(path_book)

    if visualize:
        cv2.namedWindow('img', cv2.WINDOW_NORMAL)

    cap = cv2.VideoCapture(source_path)
    _, img = cap.read()
    out_name=(source_path.split('/')[-1]).split('.')[0]+'_tracking.mp4'
    w,h = img.shape[:2]
    out = cv2.VideoWriter(output_path+out_name, cv2.VideoWriter_fourcc(*"mp4v"), 30, (h*2,w))
    num_frame=0
    ret=True

    colors = []
    for i in range(num_balls):
        colors.append(getDistinctColors(i, num_balls))
    # Se reordenan los colores para separar los que son cromáticamente más parecidos e intentar evitar que aparezcan juntos
    colors_reorder = [colors[i] for i in range(0, num_balls, 3)] + [colors[i] for i in range(1, num_balls, 3)] + [colors[i] for i in range(2, num_balls, 3)]

    hist = {}
    for i in range(num_balls):
        hist[i]=[]
    while(cap.isOpened()):
        if ret==True:
            height, width, _ = img.shape
            img = cv2.copyMakeBorder(img, 0, 0, 0, img.shape[1], cv2.BORDER_CONSTANT, None, value = 0)
            for i in range(num_balls):
                try: # Las coordenadas de la bola para ese frame puede ser None y salta excepcion con la división entera, además el último índice tampoco entra
                    coords_x, coords_y = data[i][num_frame]
                    coords_x_padding = coords_x + width
                    if len(hist[i]) <= trayectory_limit:
                        hist[i].append((coords_x_padding, coords_y))
                    else:
                        hist[i].pop(0)
                        hist[i].append((coords_x_padding, coords_y))
                    
                    for coord in hist[i]:
                        cv2.circle(img, coord, 10, colors_reorder[i], -1)
                    for index, item in enumerate(hist[i]): 
                        if index == len(hist[i]) -1:
                            break
                        cv2.line(img, item, hist[i][index + 1], colors_reorder[i], 8) 

                    start_point = (coords_x-square_len//2, coords_y-square_len//2)
                    end_point = (coords_x+square_len//2, coords_y+square_len//2)
                    cv2.rectangle(img, start_point, end_point, colors_reorder[i], 4)

                    org = (coords_x+square_len//2+2, coords_y-square_len//2+2)
                    cv2.putText(img, str(i+1), org, cv2.FONT_HERSHEY_SIMPLEX, 2, colors_reorder[i], 4)
                    org_padding = (coords_x+width+square_len//2+2, coords_y-square_len//2+2)
                    cv2.putText(img, str(i+1), org_padding, cv2.FONT_HERSHEY_SIMPLEX, 2, colors_reorder[i], 4)
                    
                except: pass
            cv2.drawMarker(img, point, (0,0,0), cv2.MARKER_CROSS, thickness=4, markerSize=width)
            num_frame +=1
            out.write(img)
            if visualize:
                cv2.imshow('img', img)
                k=cv2.waitKey(0)
                if k==27: break
        else:
            break
        ret, img = cap.read()

    cap.release()
    out.release()
    if visualize:
        cv2.destroyAllWindows()

    print("Vide saved in: ", out_name)

if __name__ == "__main__":
    ss = '31'
    system = 'ColorTrackingMaxBalls'
    #system = 'BgSubstractionTracking'
    #system = 'ColorTracking'

    video_source = 'red2_AlejandroAlonso'
    #video_source = 'red_JugglingLab'

    visualize=True
    square_len=50
    trayectory_limit = 10
    file_mode=2
    point = (507, 1046)

    tracking_visualizer(ss, system, save_dir, dataset_dir, output_path, video_source=video_source, visualize=visualize, file_mode=file_mode, point=point)