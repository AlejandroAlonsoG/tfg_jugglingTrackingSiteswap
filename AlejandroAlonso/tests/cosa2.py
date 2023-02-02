import cv2
import numpy as np
import random

elems = {}
for i in range (0,1000):
    elem = (random.randint(0,2),random.randint(0,2),random.randint(0,2))
    if elem in elems:
        elems[elem] += 1
    else:
        elems[elem] = 1

""" histogram, _ = np.histogram(list, bins=256, range=(0, 256))

print(histogram) """

ordered_dict = sorted(elems.items(), key=lambda item: item[1])

print(ordered_dict)

print(max(elems, key=elems.get))