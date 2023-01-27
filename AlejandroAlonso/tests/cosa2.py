
num_balls = 5
colors = [1,2,3,4,5]

colors_reorder = []
for i in range(0,num_balls, 3):
    colors_reorder.append(colors[i])
for i in range(1,num_balls, 3):
    colors_reorder.append(colors[i])
for i in range(2,num_balls, 3):
    colors_reorder.append(colors[i])

colors_reorder2 = []
for i in range(0, num_balls, 3):
    try:
        colors_reorder2.append(colors[i])
        colors_reorder2.append(colors[i+1])
        colors_reorder2.append(colors[i+2])
    except:
        pass

colors_reorder3 = []
colors_reorder3 = [colors[i] for i in range(0, num_balls, 3)] + [colors[i] for i in range(1, num_balls, 3)] + [colors[i] for i in range(2, num_balls, 3)]

print(colors_reorder)
print(colors_reorder2)
print(colors_reorder3)
