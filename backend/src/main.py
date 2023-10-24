#FSM
import os
import time
from analyzer import Analyzer

state = 0

while True:
    match state:
        case 0:
            if os.path.exists("../../server/video.mp4"):
                state = 1
            else:
                state = 0
        case 1:
            time.sleep(2)

            obj_analyzer = Analyzer("../../server/video.mp4", "../../server/data.txt")
            obj_analyzer.run_analyzer()

            if not obj_analyzer.flag_done:
                print("\n\t*Some problem ocurred in execution :(*\n")
                state = 0
            
            if obj_analyzer.flag_done:
                state = 2
        case 2:
            #envia para o servidor/celular
            state = 3

        case 3:
            os.remove("../../server/video.mp4")
            
            state = 0

    print(f"state: {state}")