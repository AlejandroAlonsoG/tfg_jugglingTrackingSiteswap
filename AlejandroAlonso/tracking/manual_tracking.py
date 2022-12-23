import cv2, math, numpy as np
# --------------------- START PARAMETERS -----------------------
color_values = 35,30,150,185,120,255 #RED_Alex para apoyar el tracking por color
# Capture your source video
cap = cv2.VideoCapture('/home/alex/tfg_jugglingTrackingSiteswap/dataset/ss5_red_AlejandroAlonso.mp4')
# Pick a path to save the data
output_path = '/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/test_hybrid.csv'

roi_size=200
roi_factor = 2
roi_enable=False
BUFFER_MAX=300
# -------------------- END PARAMETERS ----------------------
# Parameters for the text in the user instructions
font, scale, color, thick = cv2.FONT_HERSHEY_SIMPLEX, .5, (255,0,0), 1
click_x, click_y = 0,0
click_x_old, click_y_old = 0,0
new_click = False
roi_active = False
backtracking_mode = False
def callback(event, x, y, flags, param):
    global click_x, click_y
    global click_x_old, click_y_old
    global new_click
    if event == 1:
        new_click = True
        click_x_old, click_y_old = click_x, click_y
        click_x, click_y = x,y

cv2.namedWindow('img', cv2.WINDOW_NORMAL)
cv2.setMouseCallback('img', callback)
wait_time=1
proceed_to_next_frame = True
positions = []
buffer=[]
backtracking_buffer = []
# Main loop
while True:
    # If a user has made a click
    if proceed_to_next_frame:
        if not backtracking_mode:
            # Read frame of video
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

        

    if roi_enable and roi_active:
        # Create a background that is bigger than the roi - avoid error when ball nears edge
        bg = np.zeros((img.shape[0]+roi_size, img.shape[1]+roi_size, 3), np.uint8)
        # Paste the image onto the background
        bg[int(roi_size/2):int(roi_size/2)+img.shape[0], int(roi_size/2):int(roi_size/2)+img.shape[1]] = img
        # Get the roi from the background
        roi = bg[click_y:click_y+roi_size, click_x:click_x+roi_size]
        roi_h, roi_w, _ = roi.shape
        roi = cv2.resize(roi, (roi_w * roi_factor, roi_h * roi_factor))
    



    # Show frame and wait
    if roi_enable and roi_active:
        cv2.imshow('img', roi)
    else:
        cv2.imshow('img', img)
    k = cv2.waitKey(wait_time)
    if k ==27: break
    # User Presses F4, activate backtracking
    if k == 193: 
        backtracking_mode=True
        wait_time = 1
    # User Presses F5, activate backtracking
    if k == 194: 
        backtracking_mode=False
        wait_time = 1
    # User Presses F6, advance to the next frame and wait
    if k == 195: wait_time = 0
    # User presses F7, play slowly
    if k == 196: wait_time = 65
    # User presses F8, max computer resources
    if k == 197: wait_time = 1


    if new_click:
        if roi_active:
            click_x, click_y = int(click_x/roi_factor),int(click_y/roi_factor)
            click_x, click_y = click_x_old + click_x - int(roi_size/2), click_y_old + click_y - int(roi_size/2)
        else:
            roi_active = True
        new_click = False
        proceed_to_next_frame = True
        if not backtracking_mode:
            positions.append((click_x, click_y))
        else:
            positions.pop()
        
        if len(buffer) < BUFFER_MAX:
            if not backtracking_mode:
                buffer.append(img)
        else:
            buffer.pop(0)
            buffer.append(img)
    else: 
        proceed_to_next_frame = False



print(len(positions))
cv2.destroyAllWindows()
cap.release()