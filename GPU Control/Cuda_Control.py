import numpy as np
import cv2 as cv
import argparse
import time

def is_cuda_enabled():
    print("INFO :: OpenCV version is ",cv.__version__)
    dev = cv.cuda.getCudaEnabledDeviceCount()
    if dev == 0:
        print("\nINFO :: Your device is not CUDA enabled")
    else:
        print("\nINFO :: Your device is CUDA enabled")
        print("           Enabled device count is ", dev)

def cpu_vs_gpu():
    print("This script will do the same operation on CPU and GPU and\n"
          "compare them.")
    npTmp = np.random.random((1024, 1024)).astype(np.float32)
    npMat1 = np.stack([npTmp,npTmp],axis=2)
    npMat2 = npMat1
    cuMat1 = cv.cuda_GpuMat()
    cuMat2 = cv.cuda_GpuMat()
    cuMat1.upload(npMat1)
    cuMat2.upload(npMat2)
    start_time = time.time()
    cv.cuda.gemm(cuMat1, cuMat2,1,None,0,None,1)
    print("\nCUDA TIME :: {} seconds ".format(time.time() - start_time))
    start_time = time.time()
    cv.gemm(npMat1,npMat2,1,None,0,None,1)
    print("CPU TIME  :: {} seconds ".format(time.time() - start_time))


if __name__ == "__main__":
    arg = argparse.ArgumentParser()
    arg.add_argument('--mode', type=int, required=True)
    arg = arg.parse_args()
    if arg.mode == 0:
        is_cuda_enabled()
    elif arg.mode == 1:
        cpu_vs_gpu()
    else:
        print("Enter valid mode valur, 0 or 1")