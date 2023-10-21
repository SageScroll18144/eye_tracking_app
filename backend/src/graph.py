import matplotlib.pyplot as plt

nome_arquivo = "arquivo.txt"

# Inicialize uma lista vazia para armazenar as linhas do arquivo
left_time = list()
left_pos = list()
right_time = list()
right_pos = list()

#posição x do ponto vermelho
M = int()
L = int()
R = int() 

# Abra o arquivo em modo de leitura ('r')
with open("posxtime_left.txt", "r") as arquivo:
    # Leia cada linha do arquivo e adicione à lista
    for linha in arquivo:
        # Remova o caractere de quebra de linha '\n' no final de cada linha
        linha = linha.strip().split(" ")
        left_time.append(linha[0])
        left_pos.append(linha[1])

with open("posxtime_right.txt", "r") as arquivo:
    # Leia cada linha do arquivo e adicione à lista
    for linha in arquivo:
        # Remova o caractere de quebra de linha '\n' no final de cada linha
        linha = linha.strip().split(" ")
        right_time.append(linha[0])
        right_pos.append(linha[1])

with open("sides.txt", "r") as arquivo:
    # Leia cada linha do arquivo e adicione à lista
    count = 0
    for linha in arquivo:
        if(count == 0):
            linha = linha.strip().split(" ")
            M = linha[0]
        elif(count == 1):
            linha = linha.strip().split(" ")
            R = linha[0]
        elif(count == 2):
            linha = linha.strip().split(" ")
            L = linha[0]
        count+=1

# Dados
eixo_x = [0, 1, 2, 2, 3, 4, 4, 5, 6]
#eixo_y1 = [0,0,10, 15, 13, 18, 25]
eixo_y2 = [10,10, 10, 0, 0, 0, 20, 20, 20]

print(M)
print(R)
print(L)

#aplicar transformação em M, R e L

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
# Criar o gráfico de linha
plt.plot(left_time, right_pos, label='Left eye', marker='o', color='b')
plt.plot(left_time, left_pos, label='Right eye', marker='o', color='g')
plt.plot(setpoint_time, setpoint_pos, label='Set Point', marker='o', color='r')

# Adicione rótulos e legenda
plt.xlabel('Time')
plt.ylabel('Position axis X')
plt.title('Eye position x time')
plt.legend()

# Mostrar o gráfico
plt.show()
