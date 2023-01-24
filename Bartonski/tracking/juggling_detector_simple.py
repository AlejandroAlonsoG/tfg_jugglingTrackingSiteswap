import cv2
import sys
import math
import configuration_simple as configuration

#*edit*
import sys
sys.path.insert(0, '../../AlejandroAlonso/excel_utils')
import excel_utils
system = "bartonski"
ss = "short"
#*edit*


# Arguments and Configuration --------------------------------------------------

parser = configuration.parser
argv = sys.argv[1:]
print( f"argv: {argv}" )
o = parser.parse_args( argv )
print( f"o: {o}")

# Default Values ---------------------------------------------------------------
frame_delay = 1
toggle = [1, 0]

filename = str(sys.argv[-1])

# Set-up -----------------------------------------------------------------------

## Input Video file

cap = cv2.VideoCapture(filename)
width      = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height     = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Object detection from stable camera
object_detector = cv2.createBackgroundSubtractorMOG2(
                    history=100,
                    varThreshold=40)

current_frame = 0

# Helper Functions for Video Read Loop -----------------------------------------

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

# frame objects have an object id, a center and a 'seen' field.
last_frame_objects = []
object_id=0
def track( contours):
    #*edit*print( f"contours: {contours}")
    frame_objects = []
    global object_id
    global last_frame_objects
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 100: # Comprueba que el contorno sea mayor al area minima seleccionada
            frame_object = {}
            frame_object["center"]=get_center(contour)
            frame_object["seen"]=False
            frame_object["contour"] = contour
            frame_object["area"] = area
            frame_object["type"] = 'throw'
            for lfo in last_frame_objects:
                offset_x = frame_object["center"][0] - lfo["center"][0]
                offset_y = frame_object["center"][1] - lfo["center"][1]
                if ( math.hypot(offset_x, offset_y) <= 20 # Comprueba que el objeto no esté demasiado lejos del anterior visto
                     and frame_object["type"] is not None ):
                    frame_object["object_id"] = lfo["object_id"] # Asigna el que está viendo con la misma etiqueta que el anterior
                    frame_object["seen"] = True # Marca que ya lo ha visto
            #print( f"frame_object: {frame_object}")
            frame_objects.append(frame_object)
    new_frame_objects = []
    # Asigna un id a cada objeto
    for fo in frame_objects:
        if fo["seen"] == False:
            object_id += 1
            fo["object_id"] = object_id
        new_frame_objects.append(fo)
    last_frame_objects = new_frame_objects.copy()
    #print( object_id )
    # Basicamente devuelve un array de diccionarios donde cada diccionario es sobre un objeto (contorno suficientemente grande) que se ha encontrado en el frame
    return new_frame_objects
# Video Read Loop --------------------------------------------------------------

ret, frame = cap.read()

book = excel_utils.book_initializer(system,ss) #*edit*
while ret:
    mask = object_detector.apply(frame) # Básicamente la máscara es aplicar BackgroundSubstractor con 100 y 40 a toda la imagen
    _, mask = cv2.threshold( mask, 254, 255, # Se pasa la máscara por un threshold de grises
                                cv2.THRESH_BINARY )
    contours, _ = cv2.findContours( mask, # Desde el resultado de esa máscara se sacan los contornos
                                    cv2.RETR_TREE,
                                    cv2.CHAIN_APPROX_SIMPLE )

    window_label = "Frame"
    image = frame

    tracked_objects=track(contours)
    #*edit*print(f"tracked_objects: {tracked_objects}")
    # tracked_objects basicamente es un array de diccionarios donde cada diccionario es sobre un objeto (contorno suficientemente grande) que se ha encontrado en el frame
    # Creo que este frame lo que hace basicamente es pintar todo
    for to in tracked_objects:
        # print(f"to: {to}")
        cv2.drawContours(image, [to["contour"]], -1, (0, 255, 0), 2)
        oid=to["object_id"]
        #*edit*print(f"to[object_id]: {oid} to[center] {to['center']}")
        excel_utils.book_writer(book, current_frame, oid, to['center']) #*edit*
        object_labels( image, f"{to['object_id']} {to['type']}", to["center"], 0, 2)

    cv2.namedWindow(window_label, cv2.WINDOW_NORMAL) # Create a named window
    cv2.moveWindow(window_label, 40,30)              # Move it to (40,30)
    cv2.imshow(window_label, image)

    key = cv2.waitKey(frame_delay)

    ret, frame = cap.read()
    current_frame += 1

excel_utils.book_saver(book,system,ss, sanitize=False)  #*edit*

cap.release()
cv2.destroyAllWindows()
