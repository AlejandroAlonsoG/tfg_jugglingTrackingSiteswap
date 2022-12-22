import cv2
import os
import sys
import re
import getopt
import math
import json
import numpy as np
import configuration

#*edit*
import sys
sys.path.insert(0, '/media/alex/ELISA_DD/TFG/AlejandroAlonso/excel_utils')
import excel_utils
system = "bartonski"
ss = "5"
#*edit*


# Arguments and Configuration --------------------------------------------------

parser = configuration.parser
argv = sys.argv[1:]
print( f"argv: {argv}" )
o = parser.parse_args( argv )
print( f"o: {o}")

# Default Values ---------------------------------------------------------------

trails = not o.no_trails
trails_color = (    0,    0, 0xFF )
grid_color =   ( 0x7F, 0x7F, 0x7F )
grid_width = 2
frame_delay = 1
toggle = [1, 0]
throw_mask = None
left_hand_mask = None
right_hand_mask = None

filename = str(sys.argv[-1])

# Set-up -----------------------------------------------------------------------

## Input Video file

cap = cv2.VideoCapture(filename)
width      = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height     = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
if o.throw_roi_bottom is None:
    o.throw_roi_bottom = height-1
throw_roi_left = 0
throw_roi_right = width-1

## Output Video file

result = re.search( '(.*)\.([^.]+$)', filename )
basename, extension = result.groups()
label="detector"
output_file=f"{basename}.{label}.{extension}"

out = cv2.VideoWriter(
        output_file, cv2.VideoWriter_fourcc('m','p','4','v'),
        frame_rate/2, (width, height)
      )

## Mask files

if o.write_throw_mask is not None:
    throw_mask = f"{basename}.throw_mask.png"
if o.write_left_hand_mask is not None:
    left_hand_mask = f"{basename}.left_hand_mask.png"
if o.write_right_hand_mask is not None:
    right_hand_mask = f"{basename}.right_hand_mask.png"

if o.end_frame is None:
    o.end_frame = frame_count

# Object detection from stable camera
object_detector = cv2.createBackgroundSubtractorMOG2(
                    history=o.detector_history,
                    varThreshold=o.detector_threshold)

## Trails image
trails_mask = np.zeros( [height, width, 1], dtype = np.uint8 ) 

## Trail color input
trails_color_image = np.zeros( [height, width, 3], dtype = np.uint8 ) 
trails_color_image[:] = trails_color

trails_image = np.zeros( [height, width, 3], dtype = np.uint8 ) 

## Trails image
trails_write_mask = {
    'throw': np.zeros( [height, width, 1], dtype = np.uint8 ),
    'left_hand': np.zeros( [height, width, 1], dtype = np.uint8 ),
    'right_hand': np.zeros( [height, width, 1], dtype = np.uint8 ) 
}


print( f"size: {width}x{height}")
print( f"video frame count: {frame_count}")
print( f"options: {o}")
print( f"selection frame count: {o.end_frame-o.start_frame}")

current_frame = 0
centers = []

# Read mask files --------------------------------------------------------------
def open_read_mask_file( mask_file ):
    read_mask = None
    if mask_file is not None:
        maskimg = cv2.imread( mask_file )
        read_mask = cv2.cvtColor(maskimg, cv2.COLOR_RGB2GRAY)
    else:
        # if no read file is given, return white mask.
        read_mask = np.zeros( [height, width, 1], dtype = np.uint8 )
        read_mask[:] = 255
    return read_mask

read_masks = {
    'throw':      open_read_mask_file(o.throw_read_mask),
    'left_hand':  open_read_mask_file(o.left_hand_read_mask),
    'right_hand': open_read_mask_file(o.right_hand_read_mask)
}

# Helper Functions for Video Read Loop -----------------------------------------

def show_grid( image ):
    # Draw horizontal lines
    for y in range(0, height, o.grid_spacing):
        cv2.line(image, ( 0, y), (width, y), grid_color, grid_width  )
    # Draw vertical lines
    for x in range(0, width, o.grid_spacing):
        cv2.line(image, ( x, 0), (x, height), grid_color, grid_width  )

def get_center( contour ):
    M = cv2.moments(contour)
    return [ int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]) ]

# May want to center text, see
# https://gist.github.com/xcsrz/8938a5d4a47976c745407fe2788c813a
def object_labels( image, text, center, label_offset, shadow_offset ):
    offset=label_offset-shadow_offset
    cv2.putText(image, f"{text}", (center[0]-offset, center[1]-offset),
                cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 2 )
    offset=label_offset
    cv2.putText(image, f"{text}", (center[0]-offset, center[1]-offset),
                cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 2 )

def label( image, text, center, label_offset, shadow_offset ):
    offset=label_offset-shadow_offset
    cv2.putText(image, f"{text}", (center[0]-offset, center[1]-offset),
                cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 2 )
    offset=label_offset
    cv2.putText(image, f"{text}", (center[0]-offset, center[1]-offset),
                cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2 )

print( f"After def. area_labels: {o.area_labels}")

def read_mask_type( center, read_masks ):
    for masktype in read_masks:
        if read_masks[masktype][center[1]][center[0]] == 255:
            return masktype
    return None

# frame objects have an object id, a center and a 'seen' field.
last_frame_objects = []
object_id=0
tracking_threshold=o.tracking_threshold
def track( contours, read_masks ):
    #*edit*print( f"contours: {contours}")
    frame_objects = []
    global object_id
    global last_frame_objects
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > o.area_threshold:
            frame_object = {}
            frame_object["center"]=get_center(contour)
            frame_object["seen"]=False
            frame_object["contour"] = contour
            frame_object["area"] = area
            frame_object["type"] = read_mask_type( frame_object["center"], read_masks )
            for lfo in last_frame_objects:
                offset_x = frame_object["center"][0] - lfo["center"][0]
                offset_y = frame_object["center"][1] - lfo["center"][1]
                if ( math.hypot(offset_x, offset_y) <= tracking_threshold
                     and frame_object["type"] is not None ):
                    frame_object["object_id"] = lfo["object_id"]
                    frame_object["seen"] = True
            #print( f"frame_object: {frame_object}")
            frame_objects.append(frame_object)
    new_frame_objects = []
    for fo in frame_objects:
        if fo["seen"] == False:
            object_id += 1
            fo["object_id"] = object_id
        new_frame_objects.append(fo)
    last_frame_objects = new_frame_objects.copy()
    #print( object_id )
    return new_frame_objects
# Video Read Loop --------------------------------------------------------------

ret, frame = cap.read()

book = excel_utils.book_initializer(system,ss) #*edit*
while ret and current_frame <= o.end_frame:
    if current_frame < o.start_frame:
        ret, frame = cap.read()
        current_frame += 1
        continue

    throw_roi = frame[0 : o.throw_roi_bottom, throw_roi_left: throw_roi_right ]
    #*edit*print( f"current_frame: {current_frame}")
    if o.blur_radius is not None:
        blur_diameter = o.blur_radius * 2 + 1
        mask_input = cv2.GaussianBlur(throw_roi, (blur_diameter, blur_diameter), 0)
    else:
        mask_input = throw_roi
    mask = object_detector.apply(mask_input)
    _, mask = cv2.threshold( mask, o.grey_threshold-1, o.grey_threshold,
                                cv2.THRESH_BINARY )
    contours, _ = cv2.findContours( mask,
                                    cv2.RETR_TREE,
                                    cv2.CHAIN_APPROX_SIMPLE )
    if o.show_mask:
        window_label = "Mask"
        image = mask
    else:
        window_label = "Frame"
        image = frame

    if o.grid:
        show_grid( image )

    tracked_objects=track(contours, read_masks )
    #*edit*print(f"tracked_objects: {tracked_objects}")
    for to in tracked_objects:
        # print(f"to: {to}")
        centers.append(to["center"])
        c = to['center']
        cv2.circle(trails_mask, (c[0], c[1]), 2, (255), -1)
        t = to['type']
        if t is not None:
            cv2.circle(trails_write_mask[t], (c[0], c[1]), 2, (255), -1)

        if trails:
            trails_image = cv2.bitwise_and(trails_color_image, trails_color_image, mask=trails_mask)
            image = cv2.bitwise_or(image, trails_image)
        cv2.drawContours(image, [to["contour"]], -1, (0, 255, 0), 2)
        oid=to["object_id"]
        #*edit*print(f"to[object_id]: {oid} to[center] {to['center']}")
        #excel_utils.book_writer(book, current_frame, oid, to['center']) #*edit*
        object_labels( image, f"{to['object_id']} {to['type']}", to["center"], 0, 2)
        if o.area_labels:
            label( image, to["area"], to["center"], 20, 3 )

    out.write(image)
    cv2.namedWindow(window_label, cv2.WINDOW_NORMAL) # Create a named window
    cv2.moveWindow(window_label, 40,30)              # Move it to (40,30)
    cv2.imshow(window_label, image)

    key = cv2.waitKey(frame_delay)
    if key == 27:
        break
    elif key == ord(' '):
        frame_delay = toggle[frame_delay]
    elif key == ord('f'):
        frame_delay = 0

    ret, frame = cap.read()
    current_frame += 1


if throw_mask is not None:
    cv2.imwrite( throw_mask, trails_write_mask['throw'] )
if left_hand_mask is not None:
    cv2.imwrite( left_hand_mask, trails_write_mask['left_hand'] )
if right_hand_mask is not None:
    cv2.imwrite( right_hand_mask, trails_write_mask['right_hand'] )

excel_utils.book_saver(book,system,ss, sanitize=True)  #*edit*

cap.release()
out.release()
cv2.destroyAllWindows()
