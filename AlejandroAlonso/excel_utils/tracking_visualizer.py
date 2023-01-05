import sys, cv2
sys.path.insert(0, '../excel_utils')
import excel_utils as eu

source_path='/home/alex/tfg_jugglingTrackingSiteswap/dataset/ss5_red_Unknown.mp4' # Url of source video
path_book='/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/excels/tracking_short_denoise.xlsx'

source_path='/home/alex/tfg_jugglingTrackingSiteswap/dataset/tests/short.mp4' # Url of source video
#path_book='/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/excels/tracking_short_AlejandroAlonso(copy).xlsx'

#source_path='/home/alex/tfg_jugglingTrackingSiteswap/dataset/ss5_red_AlejandroAlonso.mp4' # Url of source video
#path_book='/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/excels/tracking_5_AlejandroAlonso_red.xlsx'

output_path='/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/videos/'

num_balls=8
visualize=False


data = eu.load_data(path_book)
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
        for i in range(num_balls):
            if len(data[i]) > num_frame: # Puede pasar que el tracking no llegue al ultimo frame
                print(len(data[i]), num_frame)
                coords = data[i][num_frame]
                cv2.circle(img, coords, 20, (0, 0, 255), -1)
        num_frame +=1
        out.write(img)
        if visualize:
            cv2.imshow('img', img)
            cv2.waitKey(30)
    else:
        break
    ret, img = cap.read()

cap.release()
out.release()
cv2.destroyAllWindows()