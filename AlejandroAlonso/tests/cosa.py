import numpy as np
import matplotlib.pyplot as plt

def load_data(path: str):
    ret = {}
    with open(path) as file:
        for line in file:
            frame, id, bb_left, bb_top,bounding_box_size,bounding_box_size, _, _,_,_ = [int(i) for i in line.split(',')]
            id = id-1
            if id in ret:
                if len(ret[id]) == frame-1:
                    ret[id].append((bb_left+bounding_box_size//2,bb_top+bounding_box_size//2))
                else:
                    while len(ret[id]) < frame-1:
                        ret[id].append((None,None))
                    ret[id].append((bb_left+bounding_box_size//2,bb_top+bounding_box_size//2))
            else:
                ret[id] = []
                while len(ret[id]) < frame-1:
                    ret[id].append((None,None))
                ret[id].append((bb_left+bounding_box_size//2,bb_top+bounding_box_size//2))

    return ret

# crear un diccionario con las coordenadas de cada objeto
objetos = load_data("/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/mot16/GroundTruth/3_manual.txt")


# contar el número de objetos en cada bin para los tres objetos juntos
x_coords = []
y_coords = []
for coords in objetos.values():
    x, y = zip(*coords)
    x_coords.extend(x)
    y_coords.extend(y)

hist, xedges, yedges = np.histogram2d(x_coords, y_coords, bins=50)

# crear el mapa de calor con imshow
plt.imshow(hist.T, origin='lower', extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]])
plt.colorbar()
plt.title('Mapa de calor de los tres objetos juntos')
plt.show()
