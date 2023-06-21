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
    color = 'red' if p3[0] % 2 == 0 else 'blue'
    plt.plot(curve[:, 0], curve[:, 1], color)

# Puntos hardcodeados para las 6 curvas
points_list = [
    [(0, 0), (0.5, 0.5), (1, 0)],
    [(0, 0), (1, 1), (2, 0)],
    [(0, 0), (1.5, 1.5), (3, 0)],
    [(0, 0), (2, 2), (4, 0)],
    [(0, 0), (2.5, 2.5), (5, 0)],
    [(0, 0), (3, 3), (6, 0)]
]

# Crear la figura
plt.figure(figsize=(8, 6))

# Generar las 6 curvas en la misma gráfica
for points in points_list:
    plot_curve(*points)

x = np.linspace(0, 6, 100)

# Dibujar la línea horizontal
plt.plot(x, np.zeros_like(x), color='black')

# Agregar un punto encima de la línea

# Agregar texto para los números
plt.text(-0.5, -0.25, "Tiempo:", ha='center')
plt.text(-0.5, -0.5, "Mano:", ha='center')
for num in range(7):
    plt.text(num, -0.25, str(num), ha='center')
    plt.text(num, -0.5, 'R' if num % 2 == 0 else 'L', ha='center')
    color = 'red' if num % 2 == 0 else 'blue'
    plt.plot(num, 0, marker='o', color=color)
# Etiquetas y título
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Curvas')
plt.xlim(-1,7)
plt.ylim(-2,4)

plt.plot([], [], color='red', label='Lanzamientos mano derecha')
plt.plot([], [], color='blue', label='Lanzamientos mano izquierda')
plt.legend()
# Mostrar la gráfica resultante
plt.show()
