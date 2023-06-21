import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

def plot_curve(p1, p2, p3):
    # Crear los puntos intermedios para la interpolación
    t = [0, 0.5, 1]
    x = [p1[0], p2[0], p3[0]]
    y = [p1[1], p2[1], p3[1]]

    # Realizar la interpolación cúbica
    cs = CubicSpline(t, np.vstack((x, y)).T, bc_type='natural')

    # Generar puntos en la curva
    t_new = np.linspace(0, 1, 100)
    curve = cs(t_new)

    # Dibujar la curva
    color = 'red' if p1[0] % 2 == 0 else 'blue'
    plt.plot(curve[:, 0], curve[:, 1], color)

# Puntos hardcodeados para las 6 curvas
points_list = [
    [(0, 0), (2, 0.5), (4, 0)],
    [(1, 0), (2.5, 0.5), (4, 0)]
]

# Crear la figura
plt.figure(figsize=(8, 6))

# Generar las 6 curvas en la misma gráfica
for points in points_list:
    plot_curve(*points)

x = np.linspace(0, 5, 100)

# Dibujar la línea horizontal
plt.plot(x, np.zeros_like(x), color='black')

# Agregar un punto encima de la línea

# Agregar texto para los números
plt.text(-0.5, -0.05, "Tiempo:", ha='center')
for i in range(6):
    plt.text(i, -0.05, str(i), ha='center')
    plt.plot(i, 0, marker='o', color='black')
plt.plot(0, 0, marker='o', color='red')
plt.plot(1, 0, marker='o', color='blue')
plt.plot(4, 0, marker='o', color='purple')
    

# Etiquetas y título
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Curvas')
plt.xlim(-1,6)
plt.ylim(-0.2,0.6)

plt.plot([], [], color='red', label='Lanzamiento mano derecha')
plt.plot([], [], color='blue', label='Lanzamiento mano izquierda')
plt.legend()
# Mostrar la gráfica resultante
plt.show()
