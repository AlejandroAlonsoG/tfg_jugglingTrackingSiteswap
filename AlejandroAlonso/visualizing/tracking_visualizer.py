import sys, cv2
sys.path.insert(0, '../excel_utils')
import excel_utils as eu

#source_path='/home/alex/tfg_jugglingTrackingSiteswap/dataset/tests/short.mp4' # Url of source video
#path_book='/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/tracking_3_test.xlsx'

source_path='/home/alex/tfg_jugglingTrackingSiteswap/dataset/ss5_red_AlejandroAlonso.mp4' # Url of source video
path_book='/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/tracking_5_AlejandroAlonso_red.xlsx'

num_balls=5
data = eu.load_data(path_book)

cv2.namedWindow('img', cv2.WINDOW_NORMAL)

cap = cv2.VideoCapture(source_path)
num_frame=0
while True:

    _, img = cap.read()
    # Break if the video is over
    try:
        h,w,e = img.shape
    except:
        print("Video ended")
        break

    for i in range(num_balls):
        cv2.circle(img, data[i][num_frame], 7, 200, 2)
    num_frame +=1
    cv2.imshow('img', img)
    cv2.waitKey(30)
