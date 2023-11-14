import matplotlib.pyplot as plt

LEN_WIN = 16 #cm

# ERRO NO ARG DO TOT_VIDEO

def scale_time(time, tot_video):
    return (time * tot_video) / 7000

def get_length(pixels, No_PIXELS):
    return LEN_WIN * pixels / No_PIXELS

class Graph_exp():
    def __init__(self) -> None:
        self.left_time = list()
        self.left_pos = list()
        self.right_time = list()
        self.right_pos = list()

        #posição x do ponto vermelho
        # self.M = float()
        # self.L = float()
        # self.R = float() 

        self.init_l = True
        self.initial_left_pos = -1

        self.init_r = True
        self.initial_right_pos = -1

        # with open("sides.txt", "r") as arquivo:
        #     count = 0
        #     for linha in arquivo:
        #         if(count == 0):
        #             linha = linha.strip().split(" ")
        #             self.M = float(linha[0])
        #         elif(count == 1):
        #             linha = linha.strip().split(" ")
        #             self.L = float(linha[0])
        #         elif(count == 2):
        #             linha = linha.strip().split(" ")
        #             self.R = float(linha[0])
        #         count+=1

        with open("posxtime_left.txt", "r") as arquivo:
            for linha in arquivo:
                linha = linha.strip().split(" ")
                self.left_time.append(float(linha[0]))
                self.left_pos.append(float(linha[1]))
                self.totvideo = float(linha[2]) * 1000.0
                # if self.init_l:
                #     self.initial_left_pos = float(linha[1])
                #     self.init_l = False

                # if not self.init_l:
                #     self.left_pos.append(float(linha[1]) - self.initial_left_pos)
                # else:
                #     self.left_pos.append(0)

        with open("posxtime_right.txt", "r") as arquivo:
            for linha in arquivo:
                linha = linha.strip().split(" ")
                self.right_time.append(float(linha[0]))
                self.right_pos.append(float(linha[1]))
                # if self.init_r:
                #     self.initial_right_pos = float(linha[1])
                #     self.init_r = False

                # if not self.init_r:
                #     self.right_pos.append(float(linha[1]) - self.initial_right_pos)
                # else:
                #     self.right_pos.append(0)

        #make points


    def make_points(self):
        self.setpoint_time = list()
        x = 0.0
        while x <= 7000:
            self.setpoint_time.append(x)
            x += float(7000 / len(self.left_time))
        
        print(self.setpoint_time)

        LMP_med = 0
        LRP_med = 0
        LLP_med = 0

        cnt_LMP = 0
        cnt_LRP = 0
        cnt_LLP = 0

        print(f"tot video {self.totvideo}")

        self.setpoint_left = list()
        for i in range(len(self.left_pos)):
        #     if(self.left_time[i] >= 500 and self.left_time[i] <= 2500):
        #         LMP_med += self.left_pos[i]
        #         cnt_LMP += 1
            if(self.left_time[i] >= 4300 and self.left_time[i] <= 4800):
                LRP_med += self.left_pos[i]
                cnt_LRP += 1
            elif(self.left_time[i] >= 2250 and self.left_time[i] <= 3500):
                LLP_med += self.left_pos[i]
                cnt_LLP += 1

        # self.M = float(LMP_med / cnt_LMP)
        self.R = float(LRP_med / cnt_LRP)
        self.L = float(LLP_med / cnt_LLP)

        # print(self.L)
        # print(self.M)
        # print(self.R)

        self.setpoint_pos = list()
        for x in self.setpoint_time:
            if(float(x) < 5400.0) :
                self.setpoint_pos.append(0.0) #
            # elif(float(x) < 12000.0):
            #     self.setpoint_pos.append(self.M)
            elif(float(x) < 5900.0):
                self.setpoint_pos.append(self.R)
            else:
                self.setpoint_pos.append(self.L)
        for i in range(len(self.setpoint_pos)):
            if(self.setpoint_pos[i] == self.L):
                self.setpoint_time[i] = self.setpoint_time[i-1]
                break

        print(self.setpoint_time)
    def make_graph(self):
        plt.plot(self.setpoint_time, self.setpoint_pos, label='Set Point', marker='o', color='r')
        plt.plot(self.left_time, self.left_pos, label='Left eye', marker='o', color='b')
        #plt.plot(self.right_time, self.right_pos, label='Right eye', marker='o', color='g')

        plt.xticks(rotation=90) 

        plt.xlabel('Time (ms)')
        plt.ylabel('Position axis X')
        plt.title('Eye position x time')
        plt.legend()

        plt.show()
        # plt.savefig("result")
        # plt.close()

#TESTE
graph = Graph_exp()
graph.make_points()
graph.make_graph()