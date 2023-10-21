import matplotlib.pyplot as plt

left_time = list()
left_pos = list()
right_time = list()
right_pos = list()

#posição x do ponto vermelho
M = float()
L = float()
R = float() 

with open("posxtime_left.txt", "r") as arquivo:
    for linha in arquivo:
        linha = linha.strip().split(" ")
        left_time.append(float(linha[0]))
        left_pos.append(float(linha[1]))

with open("posxtime_right.txt", "r") as arquivo:
    for linha in arquivo:
        linha = linha.strip().split(" ")
        right_time.append(float(linha[0]))
        right_pos.append(float(linha[1]))

with open("sides.txt", "r") as arquivo:
    count = 0
    for linha in arquivo:
        if(count == 0):
            linha = linha.strip().split(" ")
            M = float(linha[0])
        elif(count == 1):
            linha = linha.strip().split(" ")
            R = float(linha[0])
        elif(count == 2):
            linha = linha.strip().split(" ")
            L = float(linha[0])
        count+=1

print(M)
print(R)
print(L)

setpoint_time = left_time
setpoint_pos = list()
for x in setpoint_time:
    if(float(x) <= 2000.0) :
        setpoint_pos.append(float(M))
    elif(float(x) <= 4000.0):
        setpoint_pos.append(float(R))
    else:
        setpoint_pos.append(float(L))

print(setpoint_pos)

plt.plot(setpoint_time, setpoint_pos, label='Set Point', marker='o', color='r')
plt.plot(left_time, right_pos, label='Left eye', marker='o', color='b')
plt.plot(left_time, left_pos, label='Right eye', marker='o', color='g')


plt.xticks(rotation=90) 

plt.xlabel('Time (ms)')
plt.ylabel('Position axis X')
plt.title('Eye position x time')
plt.legend()

plt.show()
