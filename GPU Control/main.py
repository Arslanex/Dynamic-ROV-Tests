import time

from Cuda_Control import *
import os

cc = CudaControl()
si = SystemInfo()

if __name__ == "__main__":
    clear_terminal()
    print("Welcome :)\n"
          "This program developed for checking computer system and CUDA"
          "\nFor any suggestions please enter an issue in GitHub")

    while True:
        print("\n================================== MENU ===")
        print("[0] Exit")
        print("[1] System Info")
        print("[2] CUDA and FPS check")
        print("[3] Do all")
        try:
            ans0 = int(input("=> "))
        except TypeError:
            print("You have entered a wrong value,\n"
                  "exiting the program . . .")
            break

        clear_terminal()
        if(ans0 == 0):
            break

        elif(ans0 == 1):
            clear_terminal()
            print("\n================================== MENU ===")
            print("[0] Exit")
            print("[1] System info")
            print("[2] CPU info")
            print("[3] GPU info")
            print("[4] RAM info")
            print("[5] Memory info")
            print("[6] Disk info")
            print("[7] Network info")
            print("[8] Do all")

            try:
                ans1 = int(input("=> "))
            except TypeError:
                print("You have entered a wrong value,\n"
                      "Automatically selecting number 7")
                ans1 = 7

            clear_terminal()
            if(ans1 == 0):
                continue
            elif (ans1 == 1):
                si.basic_info()
            elif(ans1 == 2):
                si.cpu_info()
            elif (ans1 == 3):
                si.gpu_info()
            elif (ans1 == 4):
                si.ram_info()
            elif (ans1 == 5):
                si.memory_info()
            elif (ans1 == 6):
                si.disk_info()
            elif (ans1 == 7):
                si.network_info()
            elif (ans1 == 8):
                si.do_all()

            input("\nPress a button to continue . . .")
            clear_terminal()
        elif(ans0 == 2):
            clear_terminal()
            print("\n================================== MENU ===")
            print("[0] Exit")
            print("[1] Cuda enabled control")
            print("[2] CPU vs GPU")
            print("[3] FPS test")
            print("[4] Do all")

            try:
                ans1 = int(input("=> "))
            except TypeError:
                print("You have entered a wrong value,\n"
                      "Automatically selecting number 4")
                ans1 = 4

            clear_terminal()
            if (ans1 == 0):
                continue
            elif (ans1 == 1):
                cc.is_cuda_enabled()
            elif (ans1 == 2):
                cc.cpu_vs_gpu()
            elif (ans1 == 3):
                ans2 = input("Please enter a video path\n"
                             "=> ")
                if(os.path.exists(ans2)):
                    ans3 = input("Please select a device"
                                 "\n-> cpu"
                                 "\n-> gpu")
                    cc.fps_test(ans3, ans2)
                else:
                    print("Couldn't find the video, please check your input or "
                          "\n create an issue on github")
            elif (ans1 == 4):
                ans2 = input("Please enter a video path\n"
                             "=> ")
                if (os.path.exists(ans2)):
                    cc.do_all("gpu", ans2)
                else:
                    print("Couldn't find the video, please check your input or "
                          "\n create an issue on github")
                    ans4 = input("Dou you want to continue [Y/N]")
                    if(ans4 == "y" or ans4 == "Y" or ans4 == ""):
                        cc.is_cuda_enabled()
                        cc.cpu_vs_gpu()

            input("\nPress a button to continue . . .")
            clear_terminal()