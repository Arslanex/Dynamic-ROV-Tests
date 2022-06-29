import numpy as np
import cv2 as cv
import time
import os

def is_cuda_enabled():
    print("OpenCV version :: ", cv.__version__)
    dev = cv.cuda.getCudaEnabledDeviceCount()
    if (dev != 0):
        print("OpenCV CUDA uyumlu\n"
              "Kullanılabilir cihaz sayısı: ", dev)
        ans0 = input("Dha fazla bilgi almak iste misiniz [Y/N]?")
        if (ans0 == "Y" or ans0 == "y" or ans0 == ""):
            os.system("nvidia-smi")
    else:
        print("OpenCV CUDA uyumlu değil.")

    return dev

def cpu_vs_gpu():
    print("CPU ve GPU üzerinde aynı işlem gerçekleştirelecek perormansları karşılaştırılacak.")
    npTmp = np.random.random((1024, 1024)).astype(np.float32)
    npMat1 = np.stack([npTmp, npTmp], axis=2)
    npMat2 = npMat1
    cuMat1 = cv.cuda_GpuMat()
    cuMat2 = cv.cuda_GpuMat()
    cuMat1.upload(npMat1)
    cuMat2.upload(npMat2)
    start_time = time.time()
    cv.cuda.gemm(cuMat1, cuMat2, 1, None, 0, None, 1)
    print("\nGPU Süresi :: {} saniye ".format(time.time() - start_time))
    start_time = time.time()
    cv.gemm(npMat1, npMat2, 1, None, 0, None, 1)
    print("CPU Süresi  :: {} saniye ".format(time.time() - start_time))

def fps_test(device, video):
    timers = {
        "full pipeline": [],
        "reading": [],
        "pre-process": [],
        "optical flow": [],
        "post-process": [],
    }
    cap = cv.VideoCapture(video)
    fps = cap.get(cv.CAP_PROP_FPS)
    num_frames = cap.get(cv.CAP_PROP_FRAME_COUNT)
    ret, previous_frame = cap.read()
    if device == "cpu":
        if ret:
            frame = cv.resize(previous_frame, (960, 540))
            previous_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            hsv = np.zeros_like(frame, np.float32)
            hsv[..., 1] = 1.0
            while True:
                start_full_time = time.time()
                start_read_time = time.time()
                ret, frame = cap.read()
                end_read_time = time.time()
                timers["reading"].append(end_read_time - start_read_time)
                if not ret:
                    break
                start_pre_time = time.time()
                frame = cv.resize(frame, (960, 540))
                current_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                end_pre_time = time.time()
                timers["pre-process"].append(end_pre_time - start_pre_time)
                start_of = time.time()
                flow = cv.calcOpticalFlowFarneback(
                    previous_frame, current_frame, None, 0.5, 5, 15, 3, 5, 1.2, 0,
                )
                end_of = time.time()
                timers["optical flow"].append(end_of - start_of)
                start_post_time = time.time()
                magnitude, angle = cv.cartToPolar(
                    flow[..., 0], flow[..., 1], angleInDegrees=True,
                )
                hsv[..., 0] = angle * ((1 / 360.0) * (180 / 255.0))
                hsv[..., 2] = cv.normalize(
                    magnitude, None, 0.0, 1.0, cv.NORM_MINMAX, -1,
                )
                hsv_8u = np.uint8(hsv * 255.0)
                bgr = cv.cvtColor(hsv_8u, cv.COLOR_HSV2BGR)
                previous_frame = current_frame
                end_post_time = time.time()
                timers["post-process"].append(end_post_time - start_post_time)
                end_full_time = time.time()
                timers["full pipeline"].append(end_full_time - start_full_time)
                cv.imshow("original", frame)
                cv.imshow("result", bgr)
                k = cv.waitKey(1)
                if k == 27:
                    break
    elif device == "gpu":
        if ret:
            frame = cv.resize(previous_frame, (960, 540))
            gpu_frame = cv.cuda_GpuMat()
            gpu_frame.upload(frame)
            previous_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            gpu_previous = cv.cuda_GpuMat()
            gpu_previous.upload(previous_frame)
            gpu_hsv = cv.cuda_GpuMat(gpu_frame.size(), cv.CV_32FC3)
            gpu_hsv_8u = cv.cuda_GpuMat(gpu_frame.size(), cv.CV_8UC3)
            gpu_h = cv.cuda_GpuMat(gpu_frame.size(), cv.CV_32FC1)
            gpu_s = cv.cuda_GpuMat(gpu_frame.size(), cv.CV_32FC1)
            gpu_v = cv.cuda_GpuMat(gpu_frame.size(), cv.CV_32FC1)
            gpu_s.upload(np.ones_like(previous_frame, np.float32))
            while True:
                start_full_time = time.time()
                start_read_time = time.time()
                ret, frame = cap.read()
                gpu_frame.upload(frame)
                end_read_time = time.time()
                timers["reading"].append(end_read_time - start_read_time)
                if not ret:
                    break
                start_pre_time = time.time()
                gpu_frame = cv.cuda.resize(gpu_frame, (960, 540))
                gpu_current = cv.cuda.cvtColor(gpu_frame, cv.COLOR_BGR2GRAY)
                end_pre_time = time.time()
                timers["pre-process"].append(end_pre_time - start_pre_time)
                start_of = time.time()
                gpu_flow = cv.cuda_FarnebackOpticalFlow.create(
                    5, 0.5, False, 15, 3, 5, 1.2, 0,
                )
                gpu_flow = cv.cuda_FarnebackOpticalFlow.calc(
                    gpu_flow, gpu_previous, gpu_current, None,
                )
                end_of = time.time()
                timers["optical flow"].append(end_of - start_of)
                start_post_time = time.time()
                gpu_flow_x = cv.cuda_GpuMat(gpu_flow.size(), cv.CV_32FC1)
                gpu_flow_y = cv.cuda_GpuMat(gpu_flow.size(), cv.CV_32FC1)
                cv.cuda.split(gpu_flow, [gpu_flow_x, gpu_flow_y])
                gpu_magnitude, gpu_angle = cv.cuda.cartToPolar(
                    gpu_flow_x, gpu_flow_y, angleInDegrees=True,
                )
                gpu_v = cv.cuda.normalize(gpu_magnitude, 0.0, 1.0, cv.NORM_MINMAX, -1)
                angle = gpu_angle.download()
                angle *= (1 / 360.0) * (180 / 255.0)
                gpu_h.upload(angle)
                cv.cuda.merge([gpu_h, gpu_s, gpu_v], gpu_hsv)
                gpu_hsv.convertTo(cv.CV_8U, 255.0, gpu_hsv_8u, 0.0)
                gpu_bgr = cv.cuda.cvtColor(gpu_hsv_8u, cv.COLOR_HSV2BGR)
                frame = gpu_frame.download()
                bgr = gpu_bgr.download()
                gpu_previous = gpu_current
                end_post_time = time.time()
                timers["post-process"].append(end_post_time - start_post_time)
                end_full_time = time.time()
                timers["full pipeline"].append(end_full_time - start_full_time)
                cv.imshow("original", frame)
                cv.imshow("result", bgr)
                k = cv.waitKey(1)
                if k == 27:
                    break
    cap.release()
    cv.destroyAllWindows()
    print("Number of frames : ", num_frames)
    print("Elapsed time")
    for stage, seconds in timers.items():
        print("-", stage, ": {:0.3f} seconds".format(sum(seconds)))
    print("Default video FPS : {:0.3f}".format(fps))
    of_fps = (num_frames - 1) / sum(timers["optical flow"])
    print("Optical flow FPS : {:0.3f}".format(of_fps))
    full_fps = (num_frames - 1) / sum(timers["full pipeline"])
    print("Full pipeline FPS : {:0.3f}".format(full_fps))