from tracking.color_tracking_max_balls import color_tracking_max_balls
from prediction.seq_extractor import seq_extraction
from prediction.ss_prediction import prediction

siteswaps = [
    ('1',1), ('3',3), ('4',4), ('5',5), ('31',2), ('51',3), ('423',3), ('441',3), ('525',4), ('531',3), ('633',4)
]
# Configuration
color_range = 35,30,150,185,120,255

print("\tss\t2\t3\t4\t5\t10\tAny")
for ss, max_balls in siteswaps:
    source_path = '/home/alex/tfg_jugglingTrackingSiteswap/dataset/ss'+ss+'_red_AlejandroAlonso.mp4'
    # Tracking
    ids = color_tracking_max_balls(source_path, color_range, max_balls=max_balls, visualize=False)

    # SS
    throw_seq = seq_extraction(ids)

    ss2 = prediction(throw_seq,test_numbers=2)
    ss3 = prediction(throw_seq,test_numbers=3)
    ss4 = prediction(throw_seq,test_numbers=4)
    ss5 = prediction(throw_seq,test_numbers=5)
    ss10 = prediction(throw_seq,test_numbers=10)
    """
        BUSCANDO SS PERFECTO
        ss      2       3       4       5       10      Any
        1       True    True    True    True    True    True
        3       True    True    True    True    False   True
        4       True    True    True    True    False   True
        5       True    True    False   False   False   True
        31      False   False   True    False   False   True
        51      False   False   False   False   False   False
        423     False   False   False   False   False   False
        441     False   False   True    True    False   True
        525     False   False   False   False   False   False
        531     False   False   False   False   False   False
        633     False   False   False   False   False   False
        BUSCANDO QUE AL MENOS ESTE INCORPORADO AL RESULTADO
        ss      2       3       4       5       10      Any
        1       True    True    True    True    True    True
        3       True    True    True    True    False   True
        4       True    True    True    True    False   True
        5       True    True    False   False   False   True
        31      False   False   True    True    False   True
        51      False   False   False   False   False   False
        423     False   False   False   False   False   False
        441     False   False   True    True    True    True
        525     False   True    False   False   False   True
        531     False   False   False   False   False   False
        633     False   False   False   False   False   False
    """
    print("\t{}\t{}\t{}\t{}\t{}\t{}".format(ss,ss in ss2,ss in ss3,ss in ss4,ss in ss5,ss in ss10, ss in ss2 or ss in ss3 or ss in ss4 or ss in ss5 or ss in ss10))
""" 
print("Orden de los lanzamientos: ", throw_seq)
print("Siteswap obtenido2: ", ss2)
print("Siteswap obtenido3: ", ss3)
print("Siteswap obtenido4: ", ss4)
print("Siteswap obtenido5: ", ss5)
print("Siteswap obtenido10: ", ss10) """
