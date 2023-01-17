import itertools

def prediction(period: int, throw_order: list()) -> str:
    ss = ''
    i=1
    while len(ss)<period:
        #list.index(element, start, end), busca la bola i a partir del indice i (la primera aparicion deberia estar en i-1)
        next_throw = throw_order.index(i, i)
        ss += str(next_throw-(i-1))
        i+=1

    return ss

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
