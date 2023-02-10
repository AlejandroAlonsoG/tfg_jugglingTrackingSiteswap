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



# TODO optimizarlo, si encuentro el periodo, puedo devolver el índice en el que se ha encontrado y a partir de ahí buscar el siteswap en vez de buscarlo desde el principio
def prediction(throw_order: list(), test_numbers=10) -> str:
    ss = ''
    for i in range(len(throw_order)):
        #list.index(element, start, end), busca la bola i a partir del indice i (la primera aparicion deberia estar en i-1)
        try:
            next_throw = throw_order.index(throw_order[i], i+1)
        except:
            break
        ss += str(next_throw-i)
        i+=1
    # El periodo maximo es la longitud entre 2 porque el ss se tiene que repetir al menos 2 veces
    max_period = (len(ss)//2)
    # El numero de comprobaciones es el recibido por parametro o el mas grande posible
    if len(ss) <= max_period+test_numbers:
        test_numbers = len(ss)-max_period

    period, index = get_min_period(ss, max_period, test_numbers)

    if period is None:
        return "NotFound"

    # Comprueba la primera secuencia correcta de longitud=periodo y la devuelve como ss
    for i in range(index, len(ss)-period):
        sum_values = 0
        for j in range(period):
            sum_values += int(ss[i+j])
        if ss_validity_checker(ss[i:i+period],sum_values/period) == True:
            return ss[i:i+period]
    return "NotFound"

def ss_validity_checker(ss: str, numBalls: int) -> bool:
    # La media del ss es el numero de bolas
    totalSum = 0
    for c in ss:
        totalSum += int(c)

    if totalSum/len(ss) != numBalls:
        return False
    
    # Ninguna cifra puede estar seguida N turnos despues por otra cifra que sea N turnos menor
    start=0
    while start<len(ss):
        for c in itertools.islice(ss,start+1,None):
            idx = ss.index(c, start+1)
            tmp1 = int(ss[idx])
            tmp2 = int(ss[start])
            if(int(ss[start])-int(ss[idx]) == idx-start):
                return False
        start+=1

    return True
