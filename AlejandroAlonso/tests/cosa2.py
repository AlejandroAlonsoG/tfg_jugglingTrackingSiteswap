import cv2
import numpy as np
import matplotlib.pyplot as plt

# crear el objeto BackgroundSubtractorMOG2
fgbg = cv2.createBackgroundSubtractorMOG2()

# abrir el video
cap = cv2.VideoCapture('/home/alex/tfg_jugglingTrackingSiteswap/dataset/ss3_red_AlejandroAlonso.mp4')

# contar el número de objetos en cada bin para cada frame
hist = None
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # aplicar BackgroundSubtractorMOG2 para obtener la máscara de movimiento
    fgmask = fgbg.apply(frame)
    
    # aplicar un filtro gaussiano para suavizar la máscara
    fgmask = cv2.GaussianBlur(fgmask, (21, 21), 0)
    
    # aplicar un umbral para obtener la máscara binaria
    thresh = cv2.threshold(fgmask, 128, 255, cv2.THRESH_BINARY)[1]
    
    # encontrar los contornos de la máscara binaria
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # crear una lista con todas las coordenadas de los contornos
    coords = []
    for cnt in contours:
        for pt in cnt.reshape(-1, 2):
            coords.append((pt[0], pt[1]))

    # contar el número de objetos en cada bin del mapa
    if len(coords)>0:
        x_coords, y_coords = zip(*coords)
    
        hist_frame, xedges, yedges = np.histogram2d(x_coords, y_coords, bins=50)
        
        if hist is None:
            hist = hist_frame
        else:
            hist += hist_frame

# liberar el objeto de captura
cap.release()

# crear el mapa de calor con imshow
plt.imshow(hist.T, origin='lower', extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]])
plt.colorbar()
plt.title('Mapa de calor del movimiento en el video')
plt.show()
