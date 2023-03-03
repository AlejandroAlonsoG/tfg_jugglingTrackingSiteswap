data = {}

with open("/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/mot16/Optimizer/res_distancia.txt", "r") as file:
    # Leer la primera línea (encabezados) y descartarla
    file.readline()
    
    # Inicializar la variable de conteo
    count = 0
    curr_ss = '0'
    
    # Iterar sobre cada línea restante en el archivo
    for line in file:
        # Separar la línea en campos
        fields = line.split()
        
        # Asignar cada campo a una variable
        ss = fields[0]
        num_frag = fields[1]
        num_miss = fields[2]
        fp = fields[3]
        num_sw = fields[4]
        num_obj = fields[5]
        mostly_lost = fields[6]
        partially_tracked = fields[7]
        mostly_tracked = fields[8]
        recall = fields[9]
        precision = fields[10]
        mota = fields[11]
        motp = fields[12]
        
        # Incrementar la variable de conteo y reiniciarla si se encuentra un nuevo valor de ss
        count += 1
        if ss != curr_ss:
            count = 1
            curr_ss = ss
        # Agregar los datos a la entrada correspondiente del diccionario
        if ss in data:
            data[ss].append((count, num_sw, num_frag, num_miss, fp, num_obj, mostly_lost, partially_tracked, mostly_tracked, recall, precision, mota, motp))
        else:
            data[ss] = [(count, num_sw, num_frag, num_miss, fp, num_obj, mostly_lost, partially_tracked, mostly_tracked, recall, precision, mota, motp)]
        
        
# Imprimir los 10 mejores num_sw junto con los otros parámetros y el número de línea para cada valor de ss
for ss in data:
    # Ordenar los valores de num_sw
    sorted_data = sorted(data[ss], key=lambda x: float(x[1]), reverse=False)
    
    # Imprimir los 10 mejores num_sw junto con los otros parámetros y el número de línea
    print("Mejores resultados para ss =", ss)
    for i in range(min(len(sorted_data), 10)):
        count, num_sw, num_frag, num_miss, fp, num_obj, mostly_lost, partially_tracked, mostly_tracked, recall, precision, mota, motp = sorted_data[i]
        print("Línea", count, num_sw, num_frag, num_miss, fp, num_obj, mostly_lost, partially_tracked, mostly_tracked, recall, precision, mota, motp)

import matplotlib.pyplot as plt

# Generar la gráfica
for ss in data:
    # Obtener los valores de count y num_sw para cada línea en ss
    counts = [x[0] for x in data[ss]]
    num_sws = [float(x[1]) for x in data[ss]]
    
    # Graficar los valores para ss
    plt.plot(counts, num_sws, label="ss " + ss)

# Agregar leyendas y etiquetas a la gráfica
plt.legend()
plt.xlabel("Count")
plt.ylabel("Num_sw")
plt.title("Número de cambios de id para cada distancia")
plt.show()
