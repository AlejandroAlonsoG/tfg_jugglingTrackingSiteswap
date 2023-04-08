#------------------------------  HEADER  ------------------------------+
# This program implements manual tracking to label videos of jugglers  |
#                                                                      |
# Author: Alejandro Alonso García                                      |
# Full proyect repository:                                             |
#                                                                      |
# Most of the code in this file comes from Stephen Meschke "juggling"  |
#  repo which you can find in: https://github.com/smeschke/juggling     |
#----------------------------------------------------------------------+

import cv2, numpy as np
import data_saver_files.excel_utils as eu
import data_saver_files.mot16_utils as mu


#------------------------------ START PARAMETERS ------------------------------+

color_values = 35,30,150,185,120,255 #red_AlejandroAlonso to help with color_tracking

#source_path='/home/alex/tfg_jugglingTrackingSiteswap/dataset/ss423_red_AlejandroAlonso.mp4' # Url of source video

sys_name = 'manual' # Name of system used for naming the excel book with the results
ss = '5' # siteswap juggled for naming the excel book with the results
num_balls = 5 # Number of balls to track
source_path='/home/alex/tfg_jugglingTrackingSiteswap/dataset/ss'+ss+'_red_AlejandroAlonso.mp4'

roi_size=200 # Size of the ROI (Region Of Interest)
roi_factor = 2 # Factor of the ROI (Region Of Interest)
roi_enable=True # Enables de ROI when labeling frames

BUFFER_MAX=300 # Max size of backtracking buffer


saving_mode = 2 # -1 None, 1 excel, 2 mot16

#------------------------------ END PARAMETERS ------------------------------+

# Global variables:
click_x, click_y = 0,0 # Last click coords
click_x_old, click_y_old = 0,0 # Previous click coords
new_click = False # Check if any new click has occurred

# This callback is called every new click.
# It updates the click coords and set the new_click flag to True
def callback(event, x, y, flags, param):
    global click_x, click_y
    global click_x_old, click_y_old
    global new_click
    if event == 1:
        new_click = True
        click_x_old, click_y_old = click_x, click_y
        click_x, click_y = x,y


font, scale, color, thick = cv2.FONT_HERSHEY_SIMPLEX, .5, (255,0,0), 1

cv2.namedWindow('img', cv2.WINDOW_NORMAL)
cv2.setMouseCallback('img', callback)

backtracking_mode = False
wait_time=1
proceed_to_next_frame = True
all_positions = {}

# Track 1 ball at a time
for i in range(num_balls):
    positions = [] # All coords of this iteration
    buffer=[] # Buffer to enable backtracking
    backtracking_buffer = [] # Buffer to review backtracked frames

    cap = cv2.VideoCapture(source_path)
    video_len = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    roi_active = False
    # Main loop
    while True:
        # If a user has made a click
        if proceed_to_next_frame:
            # If backtracking, read from the buffer, else, review backtracked frames (if any) and read from video
            if not backtracking_mode:
                if len(backtracking_buffer)>0:
                    img = backtracking_buffer.pop()
                else:
                    _, img = cap.read()
            else:
                backtracking_buffer.append(img)
                img = buffer.pop()

            # Break if the video is over
            try:
                h,w,e = img.shape
            except:
                print("Video ended")
                break

        # Print instructions
        cv2.putText(img, "Click on the ball to mark its coordenates and go to next frame", (50,40), font, scale, color, thick, cv2.LINE_AA)
        cv2.putText(img, "Press F4 to activate backtracking mode", (50,80), font, scale, color, thick, cv2.LINE_AA)
        cv2.putText(img, "Press F5 to disable backtracking mode", (50,120), font, scale, color, thick, cv2.LINE_AA)
        cv2.putText(img, "Iteration frames left: {}".format(video_len-len(positions)), (50,160), font, scale, color, thick, cv2.LINE_AA)

        # Draw the previous ball positions on the screen
        try:
            for idx in range(35):
                a = positions[-(idx+2)][0], positions[-(idx+2)][1]
                b = positions[-(idx+1)][0], positions[-(idx+1)][1]
                cv2.line(img, a,b, (0,255,255), 3)
                cv2.circle(img, b, 2, 255, 2)
        except: pass

        # Draw previous balls tracked
        for j in range(i-1,-1,-1):
            cv2.circle(img, all_positions[j][len(positions)], 7, 200, 2)

        # If ROI, calculate it
        if roi_enable and roi_active:
            # Create a background that is bigger than the roi - avoid error when ball nears edge
            bg = np.zeros((img.shape[0]+roi_size, img.shape[1]+roi_size, 3), np.uint8)
            # Paste the image onto the background
            bg[int(roi_size/2):int(roi_size/2)+img.shape[0], int(roi_size/2):int(roi_size/2)+img.shape[1]] = img
            # Get the roi from the background
            roi = bg[click_y:click_y+roi_size, click_x:click_x+roi_size]
            roi_h, roi_w, _ = roi.shape
            roi = cv2.resize(roi, (roi_w * roi_factor, roi_h * roi_factor))
            # Draw iteration frames left
            cv2.putText(roi, "Iteration frames left: {}".format(video_len-len(positions)), (10,20), font, scale, color, thick, cv2.LINE_AA)

        # Show frame and wait
        if roi_enable and roi_active:
            cv2.imshow('img', roi)
        else:
            cv2.imshow('img', img)
        k = cv2.waitKey(wait_time)

        # User Presses Escape, finish iteration
        if k ==27: break
        # User Presses F4, activate backtracking
        if k == 193: 
            backtracking_mode=True
            wait_time = 1
        # User Presses F5, activate backtracking
        if k == 194: 
            backtracking_mode=False
            wait_time = 1

        # If any new click has happened
        if new_click:
            # If is the first frame, activate the roi, else, traslate roi coords to global (full image) coords
            if roi_active:
                click_x, click_y = int(click_x/roi_factor),int(click_y/roi_factor)
                click_x, click_y = click_x_old + click_x - int(roi_size/2), click_y_old + click_y - int(roi_size/2)
            else:
                roi_active = True
            new_click = False
            proceed_to_next_frame = True

            #If not backtracking, save the coords
            if not backtracking_mode:
                positions.append((click_x, click_y))
            else:
                positions.pop()
            
            # Save the frame for future backtracking
            if len(buffer) < BUFFER_MAX:
                if not backtracking_mode:
                    buffer.append(img)
            else:
                buffer.pop(0)
                buffer.append(img)
        else: 
            proceed_to_next_frame = False
    # Save this ball coords in the global dict
    all_positions[i]=positions

# Save last ball coords in the global dict
all_positions[i]=positions
cap.release()
cv2.destroyAllWindows()

# Save data to excel book
if saving_mode == 1:
    book = eu.book_initializer(sys_name, ss)
    for i in range(num_balls):
        for frame, position in enumerate(all_positions[i]):
            eu.book_writer(book, frame+1, i+1, position)
    eu.book_saver(book,sys_name, ss)
elif saving_mode == 2:
    file = mu.file_initializer(sys_name, ss, "GroundTruth")
    for frame in range(len(all_positions[0])):
        for i in range(num_balls):
            mu.file_writer(file, frame+1, i+1, all_positions[i][frame])
    mu.file_saver(file)