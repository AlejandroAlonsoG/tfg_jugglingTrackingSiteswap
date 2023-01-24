from subprocess import Popen, PIPE
import numpy as np

#subprocess.call("python3 test1.py 0.1 1 1 1 0.1 0.1", shell=True)

p = Popen(['python3', 'test1.py', '0.1', '1', '1', '1', '1', '0.1', '0.1'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
output, err = p.communicate()

ret = output.decode('ascii')[:-1]
#print(ret)
diff_x, diff_y = ret.split(' ')
diff_x = float(diff_x)
diff_y = float(diff_y)

dt, x_std_meas, y_std_meas = 0.1, 0.1, 0.1
for u_x in range(1, 32):
    print("Iter dt")
    for u_y in range(1, 32):
        print("Iter u_x")
        for std_acc in range(1, 32):
            print("Iter u_y")
            p = Popen(['python3', 'test1.py', str(dt), str(u_x), str(u_y), str(std_acc), str(x_std_meas), str(y_std_meas)], stdin=PIPE, stdout=PIPE, stderr=PIPE)
            output, err = p.communicate()

            ret = output.decode('ascii')[:-1]
            tmp_diff_x, tmp_diff_y = ret.split(' ')
            tmp_diff_x = float(tmp_diff_x)
            tmp_diff_y = float(tmp_diff_y)
            #print(tmp_diff_x, tmp_diff_y)
            if (tmp_diff_y+tmp_diff_x<diff_y+diff_x):
                print(tmp_diff_y+tmp_diff_x, "<", diff_y+diff_x)
                diff_y = tmp_diff_y
                diff_x = tmp_diff_x
                print(dt, u_x,u_y, std_acc, x_std_meas, y_std_meas)

""" dt, u_x,u_y, std_acc, x_std_meas, y_std_meas = 0.1, 10, 10, 30, 0.1, 0.1
p = Popen(['python3', 'test1.py', str(dt), str(u_x), str(u_y), str(std_acc), str(x_std_meas), str(y_std_meas)], stdin=PIPE, stdout=PIPE, stderr=PIPE)
output, err = p.communicate()
ret = output.decode('ascii')[:-1]
diff_x, diff_y = ret.split(' ')
diff_x = float(diff_x)
diff_y = float(diff_y)
print(diff_x, diff_y) """

""" while True:
    y_std_meas += 1
    p = Popen(['python3', 'test1.py', str(dt), str(u_x), str(u_y), str(std_acc), str(x_std_meas), str(y_std_meas)], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    ret = output.decode('ascii')[:-1]
    tmp_diff_x, tmp_diff_y = ret.split(' ')
    tmp_diff_x = float(tmp_diff_x)
    tmp_diff_y = float(tmp_diff_y)
    #print(tmp_diff_x, tmp_diff_y)
    if (tmp_diff_y<diff_y):
        print("y:",tmp_diff_y, "<", diff_y)
        diff_y = tmp_diff_y
        print(dt, u_x,u_y, std_acc, x_std_meas, y_std_meas)
    elif(tmp_diff_x<diff_x):
        print("x:",tmp_diff_x, "<", diff_x)
        diff_x = tmp_diff_x
        print(dt, u_x,u_y, std_acc, x_std_meas, y_std_meas)
    else:
        break
y_std_meas = 1
while True:
    y_std_meas = y_std_meas/10
    p = Popen(['python3', 'test1.py', str(dt), str(u_x), str(u_y), str(std_acc), str(x_std_meas), str(y_std_meas)], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    ret = output.decode('ascii')[:-1]
    tmp_diff_x, tmp_diff_y = ret.split(' ')
    tmp_diff_x = float(tmp_diff_x)
    tmp_diff_y = float(tmp_diff_y)
    #print(tmp_diff_x, tmp_diff_y)
    if (tmp_diff_y<diff_y):
        print("y:",tmp_diff_y, "<", diff_y)
        diff_y = tmp_diff_y
        print(dt, u_x,u_y, std_acc, x_std_meas, y_std_meas)
    elif(tmp_diff_x<diff_x):
        print("x:",tmp_diff_x, "<", diff_x)
        diff_x = tmp_diff_x
        print(dt, u_x,u_y, std_acc, x_std_meas, y_std_meas)
    else:
        break """

"""  
while True:
    u_x += 1
    p = Popen(['python3', 'test1.py', str(dt), str(u_x), str(u_y), str(std_acc), str(x_std_meas), str(y_std_meas)], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    ret = output.decode('ascii')[:-1]
    tmp_diff_x, tmp_diff_y = ret.split(' ')
    tmp_diff_x = float(tmp_diff_x)
    tmp_diff_y = float(tmp_diff_y)
    #print(tmp_diff_x, tmp_diff_y)
    if (tmp_diff_y<diff_y):
        print("y:",tmp_diff_y, "<", diff_y)
        diff_y = tmp_diff_y
        print(dt, u_x,u_y, std_acc, x_std_meas, y_std_meas)
    elif(tmp_diff_x<diff_x):
        print("x:",tmp_diff_x, "<", diff_x)
        diff_x = tmp_diff_x
        print(dt, u_x,u_y, std_acc, x_std_meas, y_std_meas)
    else:
        break
u_x = 1
while True:
    u_x = u_x/10
    p = Popen(['python3', 'test1.py', str(dt), str(u_x), str(u_y), str(std_acc), str(x_std_meas), str(y_std_meas)], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    ret = output.decode('ascii')[:-1]
    tmp_diff_x, tmp_diff_y = ret.split(' ')
    tmp_diff_x = float(tmp_diff_x)
    tmp_diff_y = float(tmp_diff_y)
    #print(tmp_diff_x, tmp_diff_y)
    if (tmp_diff_y<diff_y):
        print("y:",tmp_diff_y, "<", diff_y)
        diff_y = tmp_diff_y
        print(dt, u_x,u_y, std_acc, x_std_meas, y_std_meas)
    elif(tmp_diff_x<diff_x):
        print("x:",tmp_diff_x, "<", diff_x)
        diff_x = tmp_diff_x
        print(dt, u_x,u_y, std_acc, x_std_meas, y_std_meas)
    else:
        break


while True:
    u_y += 1
    p = Popen(['python3', 'test1.py', str(dt), str(u_x), str(u_y), str(std_acc), str(x_std_meas), str(y_std_meas)], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    ret = output.decode('ascii')[:-1]
    tmp_diff_x, tmp_diff_y = ret.split(' ')
    tmp_diff_x = float(tmp_diff_x)
    tmp_diff_y = float(tmp_diff_y)
    #print(tmp_diff_x, tmp_diff_y)
    if (tmp_diff_y<diff_y):
        print("y:",tmp_diff_y, "<", diff_y)
        diff_y = tmp_diff_y
        print(dt, u_x,u_y, std_acc, x_std_meas, y_std_meas)
    elif(tmp_diff_x<diff_x):
        print("x:",tmp_diff_x, "<", diff_x)
        diff_x = tmp_diff_x
        print(dt, u_x,u_y, std_acc, x_std_meas, y_std_meas)
    else:
        break
u_y = 1
while True:
    u_y = u_y/10
    p = Popen(['python3', 'test1.py', str(dt), str(u_x), str(u_y), str(std_acc), str(x_std_meas), str(y_std_meas)], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    ret = output.decode('ascii')[:-1]
    tmp_diff_x, tmp_diff_y = ret.split(' ')
    tmp_diff_x = float(tmp_diff_x)
    tmp_diff_y = float(tmp_diff_y)
    #print(tmp_diff_x, tmp_diff_y)
    if (tmp_diff_y<diff_y):
        print("y:",tmp_diff_y, "<", diff_y)
        diff_y = tmp_diff_y
        print(dt, u_x,u_y, std_acc, x_std_meas, y_std_meas)
    elif(tmp_diff_x<diff_x):
        print("x:",tmp_diff_x, "<", diff_x)
        diff_x = tmp_diff_x
        print(dt, u_x,u_y, std_acc, x_std_meas, y_std_meas)
    else:
        break

while True:
    std_acc += 1
    p = Popen(['python3', 'test1.py', str(dt), str(u_x), str(u_y), str(std_acc), str(x_std_meas), str(y_std_meas)], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    ret = output.decode('ascii')[:-1]
    tmp_diff_x, tmp_diff_y = ret.split(' ')
    tmp_diff_x = float(tmp_diff_x)
    tmp_diff_y = float(tmp_diff_y)
    #print(tmp_diff_x, tmp_diff_y)
    if (tmp_diff_y<diff_y):
        print("y:",tmp_diff_y, "<", diff_y)
        diff_y = tmp_diff_y
        print(dt, u_x,u_y, std_acc, x_std_meas, y_std_meas)
    elif(tmp_diff_x<diff_x):
        print("x:",tmp_diff_x, "<", diff_x)
        diff_x = tmp_diff_x
        print(dt, u_x,u_y, std_acc, x_std_meas, y_std_meas)
    else:
        break
std_acc = 1
while True:
    std_acc = std_acc/10
    p = Popen(['python3', 'test1.py', str(dt), str(u_x), str(u_y), str(std_acc), str(x_std_meas), str(y_std_meas)], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    ret = output.decode('ascii')[:-1]
    tmp_diff_x, tmp_diff_y = ret.split(' ')
    tmp_diff_x = float(tmp_diff_x)
    tmp_diff_y = float(tmp_diff_y)
    #print(tmp_diff_x, tmp_diff_y)
    if (tmp_diff_y<diff_y):
        print("y:",tmp_diff_y, "<", diff_y)
        diff_y = tmp_diff_y
        print(dt, u_x,u_y, std_acc, x_std_meas, y_std_meas)
    elif(tmp_diff_x<diff_x):
        print("x:",tmp_diff_x, "<", diff_x)
        diff_x = tmp_diff_x
        print(dt, u_x,u_y, std_acc, x_std_meas, y_std_meas)
    else:
        break

while True:
    x_std_meas += 1
    p = Popen(['python3', 'test1.py', str(dt), str(u_x), str(u_y), str(std_acc), str(x_std_meas), str(y_std_meas)], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    ret = output.decode('ascii')[:-1]
    tmp_diff_x, tmp_diff_y = ret.split(' ')
    tmp_diff_x = float(tmp_diff_x)
    tmp_diff_y = float(tmp_diff_y)
    #print(tmp_diff_x, tmp_diff_y)
    if (tmp_diff_y<diff_y):
        print("y:",tmp_diff_y, "<", diff_y)
        diff_y = tmp_diff_y
        print(dt, u_x,u_y, std_acc, x_std_meas, y_std_meas)
    elif(tmp_diff_x<diff_x):
        print("x:",tmp_diff_x, "<", diff_x)
        diff_x = tmp_diff_x
        print(dt, u_x,u_y, std_acc, x_std_meas, y_std_meas)
    else:
        break
x_std_meas = 1
while True:
    x_std_meas = x_std_meas/10
    p = Popen(['python3', 'test1.py', str(dt), str(u_x), str(u_y), str(std_acc), str(x_std_meas), str(y_std_meas)], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    ret = output.decode('ascii')[:-1]
    tmp_diff_x, tmp_diff_y = ret.split(' ')
    tmp_diff_x = float(tmp_diff_x)
    tmp_diff_y = float(tmp_diff_y)
    #print(tmp_diff_x, tmp_diff_y)
    if (tmp_diff_y<diff_y):
        print("y:",tmp_diff_y, "<", diff_y)
        diff_y = tmp_diff_y
        print(dt, u_x,u_y, std_acc, x_std_meas, y_std_meas)
    elif(tmp_diff_x<diff_x):
        print("x:",tmp_diff_x, "<", diff_x)
        diff_x = tmp_diff_x
        print(dt, u_x,u_y, std_acc, x_std_meas, y_std_meas)
    else:
        break

while True:
    y_std_meas += 1
    p = Popen(['python3', 'test1.py', str(dt), str(u_x), str(u_y), str(std_acc), str(x_std_meas), str(y_std_meas)], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    ret = output.decode('ascii')[:-1]
    tmp_diff_x, tmp_diff_y = ret.split(' ')
    tmp_diff_x = float(tmp_diff_x)
    tmp_diff_y = float(tmp_diff_y)
    #print(tmp_diff_x, tmp_diff_y)
    if (tmp_diff_y<diff_y):
        print("y:",tmp_diff_y, "<", diff_y)
        diff_y = tmp_diff_y
        print(dt, u_x,u_y, std_acc, x_std_meas, y_std_meas)
    elif(tmp_diff_x<diff_x):
        print("x:",tmp_diff_x, "<", diff_x)
        diff_x = tmp_diff_x
        print(dt, u_x,u_y, std_acc, x_std_meas, y_std_meas)
    else:
        break
y_std_meas = 1
while True:
    y_std_meas = y_std_meas/10
    p = Popen(['python3', 'test1.py', str(dt), str(u_x), str(u_y), str(std_acc), str(x_std_meas), str(y_std_meas)], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    ret = output.decode('ascii')[:-1]
    tmp_diff_x, tmp_diff_y = ret.split(' ')
    tmp_diff_x = float(tmp_diff_x)
    tmp_diff_y = float(tmp_diff_y)
    #print(tmp_diff_x, tmp_diff_y)
    if (tmp_diff_y<diff_y):
        print("y:",tmp_diff_y, "<", diff_y)
        diff_y = tmp_diff_y
        print(dt, u_x,u_y, std_acc, x_std_meas, y_std_meas)
    elif(tmp_diff_x<diff_x):
        print("x:",tmp_diff_x, "<", diff_x)
        diff_x = tmp_diff_x
        print(dt, u_x,u_y, std_acc, x_std_meas, y_std_meas)
    else:
        break """