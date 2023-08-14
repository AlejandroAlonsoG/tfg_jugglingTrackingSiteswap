from prediction.ss_prediction import prediction

data = {}
with open('./AlejandroAlonso/results/mot16/Optimizer/seq.txt', 'r') as f:
    for line in f:
        tokens= line.split("_")
        ss = tokens[0]
        l1 = tokens[1:]
        l1.append(l1.pop().split("\n")[0])

        data[ss] = []
        #print(ss, l1)
        for i in range(1, len(l1)//2):
            data[ss].append((i, ss == prediction(l1, test_numbers=i)))

#print(data)

count_dict = {}

for key in data:
    for num, flag in data[key]:
        if flag:
            count_dict[num] = count_dict.get(num, 0) + 1

import matplotlib.pyplot as plt

list_count = list(count_dict.items())

x, y = zip(*list_count)

# Crear el gráfico
plt.plot(x, y)
plt.xlabel('test_numbers')
plt.ylabel('num_aciertos')

# Mostrar el gráfico
plt.show()

""" result = lista_ordenada = sorted(list(count_dict.items()), key=lambda x: x[1], reverse=True)
print(result) """
