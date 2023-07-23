import itertools

# https://stackoverflow.com/a/46799141
#Where max_period is the maximun period you want to look for, 
# and test_numb is how many numbers of the sequence you want to test, the bigger the better but you have to make max_period+test_numb < len(sequence)
""" def get_min_period(sequence,max_period,test_numb):
    seq_len = len(sequence)
    for i in range(1,seq_len):       
        for period in range(1,max_period+1):
            found =True
            for con in range(test_numb):
                c1 = sequence[-i-con]
                c2 = sequence[-i-period-con]
                if c1 != c2:
                    found = False
                    break
            if found:           
                return period, i

    return None """

def get_min_period(sequence,max_period,test_numb):
    if max_period > len(sequence)-test_numb:
        max_period = len(sequence)-test_numb
    for period in range(1, max_period+1):
        for i in range(len(sequence)-(test_numb+period-1)):
            found =True
            for t in range(test_numb):
                c1 = sequence[i+t]
                c2 = sequence[i+t+period]
                if c1!=c2:
                    found = False
                    break
            if found:  
                return period, i
 
    return None, None



def get_full_ss_string(throw_order):
    ss = ''
    next_throw=0
    for i in range(len(throw_order)):
        #list.index(element, start, end), busca la bola i a partir del indice i (la primera aparicion deberia estar en i-1)
        try:
            next_throw = throw_order.index(throw_order[i], i+1)
        except:
            pass
        ss += str(next_throw-i)
        i+=1
    return ss

def get_ss_from_seq_non_0(throw_order: list(), test_numbers=5) -> str:
    ss = get_full_ss_string(throw_order)
    ss = ss.replace('-','')
    # El periodo maximo es la longitud entre 2 porque el ss se tiene que repetir al menos 2 veces
    max_period = (len(ss)//2)
    # El numero de comprobaciones es el recibido por parametro o el mas grande posible
    if len(ss) <= max_period+test_numbers:
        test_numbers = len(ss)-max_period

    period, index = get_min_period(ss, max_period, test_numbers)

    if period is None:
        return "NotFound", ss

    # Comprueba la primera secuencia correcta de longitud=periodo y la devuelve como ss
    for i in range(index, len(ss)-period):
        sum_values = 0
        for j in range(period):
            sum_values += int(ss[i+j])
        if ss_validity_checker(ss[i:i+period],sum_values/period) == True:
            return ss[i:i+period], ss
    return "NotFound", ss

def get_ss_from_seq_0(throw_order: list(), test_numbers=5) -> str:
    ss = get_full_ss_string(throw_order)
    ss = ''.join([char if id != -1 else '0' for char, id in zip(ss, throw_order)])
    # El periodo maximo es la longitud entre 2 porque el ss se tiene que repetir al menos 2 veces
    max_period = (len(ss)//2)
    # El numero de comprobaciones es el recibido por parametro o el mas grande posible
    if len(ss) <= max_period+test_numbers:
        test_numbers = len(ss)-max_period

    period, index = get_min_period(ss, max_period, test_numbers)

    if period is None:
        return "NotFound", ss

    # Comprueba la primera secuencia correcta de longitud=periodo y la devuelve como ss
    for i in range(index, len(ss)-period):
        sum_values = 0
        for j in range(period):
            sum_values += int(ss[i+j])
        if ss_validity_checker(ss[i:i+period],sum_values/period) == True:
            return ss[i:i+period], ss
    return "NotFound", ss

def prediction(throw_order: list(), num_balls, test_numbers=5) -> str:
    pred_list = []
    pred_list.append(get_ss_from_seq_0(throw_order, test_numbers))
    pred_list.append(get_ss_from_seq_non_0([throw_order[i+2] if throw_order[i] == -1 else throw_order[i] for i in range(1, len(throw_order)-2)], test_numbers))
    #pred_list.append(get_ss_from_seq_non_0([id for id in throw_order if id !=- 1], test_numbers))
    ret = pred_list[0]
    for pred, full_ss in pred_list[1:]:
        if pred != 'NotFound' and ss_validity_checker(pred, num_balls):
            ret = pred, full_ss

    return ret



def ss_validity_checker(ss: str, num_balls: int) -> bool:
    # La media del ss es el numero de bolas
    totalSum = 0
    for c in ss:
        totalSum += int(c)

    if totalSum/len(ss) != num_balls:
        return False
    
    # Ninguna cifra puede estar seguida N turnos despues por otra cifra que sea N turnos menor
    start=0
    while start<len(ss):
        for c in itertools.islice(ss,start+1,None):
            idx = ss.index(c, start+1)
            if(int(ss[start])-int(ss[idx]) == idx-start):
                return False
        start+=1

    return True

if __name__ == "__main__":
    #throw_order = [1,-1,2,-1,3,1,-1,2,-1,3,1,-1,2,-1,3,1,-1,2,-1,3]
    #throw_order = [1,2,3,1,2,3,1,2,3]
    throw_order = [1,2,3,2,1,3,1,2,3,2,1,3]
    print(prediction(throw_order, 3))