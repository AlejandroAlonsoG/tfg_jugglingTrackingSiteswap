import os
from metrics.motmetrics import motMetricsEnhancedCalculator
from openpyxl import Workbook

gt_path = '/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/mot16/GroundTruth/'
t_path = '/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/mot16/Tracking/'
ss=3
directory = os.fsencode(t_path)

# Crea un objeto Workbook para el archivo de Excel
workbook = Workbook()

# Crea una hoja en el archivo de Excel
worksheet = workbook.create_sheet(title='Resultados')

# Escribe los encabezados de las columnas en la primera fila
encabezados = ["ss", "min_contour", "enclosing area", "arc","T. Perdido", "D. Perdidas", "D. Ruido", "ID swap", "nBalls", "<20%", "20%80%", ">80%", "Recall", "Precision", "MOTA", "MOTP"]
worksheet.append(encabezados)

# Escribe los datos en la hoja
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    print(filename)
    toks = filename.split('_')
    ss = toks[0]
    min_contour = toks[2][len(ss):]
    enclosing_area = toks[3]
    arc = toks[4][:-4]
    if filename.endswith(".txt"):
        fila = motMetricsEnhancedCalculator(filename, gt_path+str(ss)+'_manual.txt', t_path+filename).split('\n')[-1].split()
        tmp = [ss, min_contour, enclosing_area, arc]
        tmp.extend(fila[1:])
        worksheet.append(tmp)

# Guarda el archivo de Excel
workbook.save('tabla.xlsx')
