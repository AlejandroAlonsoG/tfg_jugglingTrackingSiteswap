import sys, cv2
sys.path.insert(0, '../excel_utils')
import excel_utils as eu

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


data,num_balls = eu.load_data(path_book)
cv2.namedWindow('img', cv2.WINDOW_NORMAL)

cap = cv2.VideoCapture(source_path)
_, img = cap.read()
out_name=(source_path.split('/')[-1]).split('.')[0]+'_tracking.mp4'
w,h = img.shape[:2]
out = cv2.VideoWriter(output_path+out_name, cv2.VideoWriter_fourcc(*"mp4v"), 30, (h,w))
num_frame=0
ret=True
while(cap.isOpened()):
    if ret==True:
        """ for i in range(num_balls):
            if len(data[i]) > num_frame and data[i][num_frame][0] is not None: # Puede pasar que el tracking no llegue al ultimo frame o que para ese frame no haya datos
                print(len(data[i]), num_frame)
                coords_x, coords_y = data[i][num_frame][0], data[i][num_frame][1]
                #cv2.circle(img, coords, 20, (0, 0, 255), -1)
                start_point = (coords_x-square_len//2, coords_y-square_len//2)
                end_point = (coords_x+square_len//2, coords_y+square_len//2)
                cv2.rectangle(img, start_point, end_point, (0, 0, 255), 2)
                org = (coords_x+square_len//2+2, coords_y-square_len//2+2)
                cv2.putText(img, "Bola {}".format(i+1), org, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2) """
        for i in range(num_balls):
            try: # Las coordenadas de la bola para ese frame puede ser None y salta excepcion con la división entera, además el último índice tampoco entra
                coords_x, coords_y = data[i][num_frame]
                start_point = (coords_x-square_len//2, coords_y-square_len//2)
                end_point = (coords_x+square_len//2, coords_y+square_len//2)
                cv2.rectangle(img, start_point, end_point, (0, 0, 255), 2)
                org = (coords_x+square_len//2+2, coords_y-square_len//2+2)
                cv2.putText(img, "Bola {}".format(i+1), org, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
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