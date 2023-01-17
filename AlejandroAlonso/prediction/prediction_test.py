import ss_prediction as pred

valid_ss = [('423',3), ('441',3), ('531',3), ('633',4), ('5551',4), ('53',4), ('534',4)]
non_valid_ss = [('1231',7), ('90',9), ('43',3.5), ('651',4), ('624',4)]


for ss, numBalls in valid_ss:
    #print(ss, numBalls, "=>", pred.ss_validity_checker(ss,numBalls))
    assert(pred.ss_validity_checker(ss,numBalls) == True)

for ss, numBalls in non_valid_ss:
    #print(ss, numBalls, "=>", pred.ss_validity_checker(ss,numBalls))
    assert(pred.ss_validity_checker(ss,numBalls) == False)

ss_list = [(3,[1,2,3,2,1,3,1,2,3],'423'),
        (3,[1,2,3,3,1,2,2,3,1],'441'), 
        (3,[1,2,3,3,2,1,1,2,3], '531'),
        (3,[1,2,3,4,2,3,1,2,3,4,2,3], '633'),
        (4,[1,2,3,4,4,1,2,3,3,4,1,2,2,3,4,1], '5551'),
        (2,[1,2,3,4,2,1,4,3], '53'),
        (3,[1,2,3,4,2,1,3,2,4,1,2,3],'534')]

for period, throw_order, ss in ss_list:
    #print(ss, "=>" ,pred.prediction(period, throw_order))
    assert(ss == pred.prediction(period, throw_order))