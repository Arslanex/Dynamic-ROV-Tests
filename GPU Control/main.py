from FPS_Test import main
from Cuda_Control import *
import time
import os

if __name__ == "__main__":
    while (True):
        print("\nWhat would you like to do?\n"
              "[0] Exit\n"
              "[1] Check CUDA\n"
              "[2] Compare CPU - GPU\n"
              "[3] Run an FPS Test")

        try:
            in1 = int(input("=> "))
        except ValueError:
            pass
        finally:
            print()

        if (in1 == 0):
            print("SYSTEM :: Exiting the program . . .")
            break
        elif (in1 == 1):
            print("-"*30)
            is_cuda_enabled()
            print("-" * 30)
            time.sleep(2)
        elif (in1 == 2):
            print("-" * 30)
            cpu_vs_gpu()
            print("-" * 30)
            time.sleep(2)
        elif (in1 == 3):
            print("Please enter video directory ")
            path = input("=> ")
            if(os.path.exists(path)):
                print("Please enter device type [CPU\GPU]")
                in2 = input("=> ")
                if (in2 != "GPU" or in2 != "gpu"):
                    in2 = "cpu"
                elif (in2 == "GPU"):
                    in2 = "gpu"
                print("-" * 30)
                main(path, in2)
                print("-" * 30)
                time.sleep(2)
            else:
                print("SYSTEM :: File not found.")