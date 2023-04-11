import pandas as pd
import matplotlib.pyplot as plt

# Lee los datos del archivo Excel
df = pd.read_excel('tabla.xlsx')

# Agrupa los datos por ss y min_contour y calcula el promedio de ID swap
grouped_df = df.groupby(['ss', 'min_contour'])['ID swap'].mean()

# Crea una gráfica de barras para cada valor de ss
for ss in df['ss'].unique():
    sub_df = grouped_df.loc[ss]
    plt.bar(sub_df.index, sub_df.values, label=f'ss={ss}')

# Agrega etiquetas y leyenda
plt.xlabel('min_contour')
plt.ylabel('ID swap')
plt.legend()

# Muestra la gráfica
plt.show()
