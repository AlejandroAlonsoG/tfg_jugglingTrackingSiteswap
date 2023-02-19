import os
from metrics.motmetrics import motMetricsEnhancedCalculator

gt_path = '/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/mot16/GroundTruth/'
t_path = '/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/mot16/Optimizer/'
ss=3
directory = os.fsencode(t_path)

with open('/home/alex/tfg_jugglingTrackingSiteswap/AlejandroAlonso/results/mot16/Optimizer/resultados_emergencia.txt', 'w') as f:
    f.write("                                       T. Perdido  D. Perdidas  D. Ruido  ID swap  nBalls  <20%  20%80%  >80% Recall Precision   MOTA   MOTP\n")
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        print(filename)
        if filename.endswith(".txt"):
            f.write(motMetricsEnhancedCalculator(filename, gt_path+str(ss)+'_manual.txt', t_path+filename))
            f.write("\n")
