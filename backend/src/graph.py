import matplotlib.pyplot as plt

# Dados
eixo_x = [0, 1, 2, 2, 3, 4, 4, 5, 6]
#eixo_y1 = [0,0,10, 15, 13, 18, 25]
eixo_y2 = [10,10, 10, 0, 0, 0, 20, 20, 20]

# Criar o gráfico de linha
#plt.plot(eixo_x, eixo_y1, label='Série Y1', marker='o', color='b')
plt.plot(eixo_x, eixo_y2, label='Série Y2', marker='s', color='r')

# Adicione rótulos e legenda
plt.xlabel('Eixo X')
plt.ylabel('Eixo Y')
plt.title('Eye position')
plt.legend()

# Mostrar o gráfico
plt.show()
