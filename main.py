from CudaControl import *

if __name__ == "__main__":
    video = input("Test için lütfen video dizinini girin > ")
    dev = is_cuda_enabled()
    if (dev == 0):
        print("\nCPU ve GPU karşılaştıması gerçekleştirilemiyor.")
        print("FPS tesleri CPU üzerinden gerçelştirilecek.")
        fps_test("cpu", video)
    else:
        cpu_vs_gpu()
        fps_test("gpu", video)