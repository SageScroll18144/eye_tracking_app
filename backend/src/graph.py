import matplotlib.pyplot as plt

def scale_time(time, tot_video):
    return (time * tot_video) / 6000.0

class Graph_exp():
    def __init__(self) -> None:
        self.left_time = list()
        self.left_pos = list()
        self.right_time = list()
        self.right_pos = list()

        #posição x do ponto vermelho
        self.M = float()
        self.L = float()
        self.R = float() 

        with open("posxtime_left.txt", "r") as arquivo:
            for linha in arquivo:
                linha = linha.strip().split(" ")
                self.left_time.append(float(linha[0]))
                self.left_pos.append(float(linha[1]))

        with open("posxtime_right.txt", "r") as arquivo:
            for linha in arquivo:
                linha = linha.strip().split(" ")
                self.right_time.append(float(linha[0]))
                self.right_pos.append(float(linha[1]))

        with open("sides.txt", "r") as arquivo:
            count = 0
            for linha in arquivo:
                if(count == 0):
                    linha = linha.strip().split(" ")
                    self.M = float(linha[0])
                elif(count == 1):
                    linha = linha.strip().split(" ")
                    self.R = float(linha[0])
                elif(count == 2):
                    linha = linha.strip().split(" ")
                    self.L = float(linha[0])
                count+=1

        self.setpoint_time = self.left_time
        self.setpoint_pos = list()
        for x in self.setpoint_time:
            if(float(x) <= scale_time(2000.0, self.setpoint_time[len(self.setpoint_time)-1])) :
                self.setpoint_pos.append(float(self.M))
            elif(float(x) <= scale_time(4000.0, self.setpoint_time[len(self.setpoint_time)-1])):
                self.setpoint_pos.append(float(self.R))
            else:
                self.setpoint_pos.append(float(self.L))
        
    def make_graph(self):
        plt.plot(self.setpoint_time, self.setpoint_pos, label='Set Point', marker='o', color='r')
        plt.plot(self.left_time, self.right_pos, label='Left eye', marker='o', color='b')
        plt.plot(self.left_time, self.left_pos, label='Right eye', marker='o', color='g')


        plt.xticks(rotation=90) 

        plt.xlabel('Time (ms)')
        plt.ylabel('Position axis X')
        plt.title('Eye position x time')
        plt.legend()

        plt.show()

#TESTE
graph = Graph_exp()
graph.make_graph()