from datetime import datetime
import platform
import psutil
import GPUtil

import cv2 as cv
import numpy as np

import time
import os

class SystemInfo:
    def __init__(self):pass

    def basic_info(self):
        print("\n"+"=" * 70, "Boot Time")
        boot_time_timestamp = psutil.boot_time()
        bt = datetime.fromtimestamp(boot_time_timestamp)
        print(f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")

        print("\n"+"=" * 70, "System Info")
        print("Computer network name :: ",platform.node())
        print("Machine type :: ", platform.machine())
        print("Processor type :: ", platform.processor())
        print("Platform type :: ", platform.platform())
        print("Operating system type :: ", platform.system())
        print("Operating system release :: ", platform.release())
        print("Operating system version :: ", platform.version())

    def cpu_info(self):
        print("\n"+"=" * 70, "CPU Info")
        print("Number of physical cores :: ", psutil.cpu_count(logical=False))
        print("Number of logical cores :: ", psutil.cpu_count(logical=True))
        cpufreq = psutil.cpu_freq()
        print(f"\nMax Frequency :: {cpufreq.max:.2f}Mhz")
        print(f"Min Frequency :: {cpufreq.min:.2f}Mhz")
        print(f"Current Frequency :: {cpufreq.current:.2f}Mhz")
        print("\nCPU Usage Per Core:")
        for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
            print("Core {} : {}%".format(i+1, percentage))
        print("Total CPU Usage :: {}%".format(psutil.cpu_percent()))

    def gpu_info(self):
        print("\n"+"=" * 70, "GPU Details")
        gpus = GPUtil.getGPUs()
        for gpu in gpus:
            print("\n===== {} =====".format(gpu.name))
            print("Load :: {}%".format(gpu.load * 100))
            print("Free memory :: {}MB".format(gpu.memoryFree))
            print("Used memory :: {}MB".format(gpu.memoryUsed))
            print("Total memory ::{}MB".format(gpu.memoryTotal))
            print("Temperature :: {} °C".format(gpu.temperature))
            print("Uuid :: ",gpu.uuid)

    def ram_info(self):
        print("\n"+"=" * 70, "RAM Info")
        print("Total RAM installed :: {} GB".format(round(psutil.virtual_memory().total / 1000000000, 2)))
        print("Available RAM :: {} GB".format(round(psutil.virtual_memory().available / 1000000000, 2)))
        print("Used RAM :: {} GB".format(round(psutil.virtual_memory().used / 1000000000, 2)))
        print("RAM usage :: {}%".format(psutil.virtual_memory().percent))

    def memory_info(self):
        print("\n"+"=" * 70, "Memory Info")
        svmem = psutil.virtual_memory()
        print("Total :: {}".format(self.get_size(svmem.total)))
        print("Available :: {}".format(self.get_size(svmem.available)))
        print("Used :: {}".format(self.get_size(svmem.used)))
        print("Percentage :: {}%".format(svmem.percent))

        print("=" * 25, "SWAP")
        swap = psutil.swap_memory()
        print(f"Total: {self.get_size(swap.total)}")
        print(f"Free: {self.get_size(swap.free)}")
        print(f"Used: {self.get_size(swap.used)}")
        print(f"Percentage: {swap.percent}%")

    def disk_info(self):
        print("\n"+"=" * 70, "Disk Information")
        print("Partitions and Usage:")
        partitions = psutil.disk_partitions()
        for partition in partitions:
            print("===== Device: {} =====".format(partition.device))
            print("\tMountpoint :: {}".format(partition.mountpoint))
            print("\tFile system type :: {}".format(partition.fstype))
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                continue
            print("\tTotal Size :: {}".format(self.get_size(partition_usage.total)))
            print("\tUsed :: {}".format(self.get_size(partition_usage.used)))
            print("\tFree :: {}".format(self.get_size(partition_usage.free)))
            print("\tPercentage :: {}%".format(partition_usage.percent))
        disk_io = psutil.disk_io_counters()
        print("Total read :: {}".format(self.get_size(disk_io.read_bytes)))
        print("Total write :: {}".format(self.get_size(disk_io.write_bytes)))

    def network_info(self):
        print("\n"+"=" * 70, "Network Information")
        if_addrs = psutil.net_if_addrs()
        for interface_name, interface_addresses in if_addrs.items():
            for address in interface_addresses:
                print("\n=== Interface: {} ===".format(interface_name))
                if str(address.family) == 'AddressFamily.AF_INET':
                    print("\tIP Address :: {}".format(address.address))
                    print("\tNetmask :: {}".format(address.netmask))
                    print("\tBroadcast IP :: {}".format(address.broadcast))
                elif str(address.family) == 'AddressFamily.AF_PACKET':
                    print("\tMAC Address :: {}".format(address.address))
                    print("\tNetmask :: {}".format(address.netmask))
                    print("\tBroadcast MAC :: {}".format(address.broadcast))
        net_io = psutil.net_io_counters()
        print("Total Bytes Sent: {}".format(self.get_size(net_io.bytes_sent)))
        print("Total Bytes Received: {}".format(self.get_size(net_io.bytes_recv)))

    def get_size(self, bytes, suffix="B"):
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor

    def do_all(self):
        self.basic_info()
        ans = input("\nPress a button to continue . . .")
        if (ans != "q" and ans != "Q"):
            self.cpu_info()
            ans = input("\nPress a button to continue . . .")
            if (ans != "q" and ans != "Q"):
                self.gpu_info()
                ans = input("\nPress a button to continue . . .")
                if (ans != "q" and ans != "Q"):
                    self.ram_info()
                    ans = input("\nPress a button to continue . . .")
                    if (ans != "q" and ans != "Q"):
                        self.memory_info()
                        ans = input("\nPress a button to continue . . .")
                        if (ans != "q" and ans != "Q"):
                            self.disk_info()
                            ans = input("\nPress a button to continue . . .")
                            if (ans != "q" and ans != "Q"):
                                self.network_info()

class CudaControl:
    def __init__(self):
        self.cudaEnabled = False

    def is_cuda_enabled(self):
        gpus = GPUtil.getGPUs()
        for gpu in gpus:
            print("GPU :: ",gpu.name)
        print("OpenCV version :: ",cv.__version__)
        dev = cv.cuda.getCudaEnabledDeviceCount()
        if(dev != 0):
            self.cudaEnabled = True
            print("OpenCV is CUDA enabled\n"
                  "Enabled device count is ", dev)
            ans0 = input("Do you want more information [Y/N]?")
            if(ans0 == "Y" or ans0 == "y" or ans0 == ""):
                os.system("nvidia-smi")
        else:
            print("OpenCV is not CUDA enabled")
            self.cudaEnabled = False

    def cpu_vs_gpu(self):
        print("GPU and CPU will be compared by performing the same operations on them")
        npTmp = np.random.random((1024, 1024)).astype(np.float32)
        npMat1 = np.stack([npTmp, npTmp], axis=2)
        npMat2 = npMat1
        cuMat1 = cv.cuda_GpuMat()
        cuMat2 = cv.cuda_GpuMat()
        cuMat1.upload(npMat1)
        cuMat2.upload(npMat2)
        start_time = time.time()
        cv.cuda.gemm(cuMat1, cuMat2, 1, None, 0, None, 1)
        print("\nCUDA TIME :: {} seconds ".format(time.time() - start_time))
        start_time = time.time()
        cv.gemm(npMat1, npMat2, 1, None, 0, None, 1)
        print("CPU TIME  :: {} seconds ".format(time.time() - start_time))

    def fps_test(self, device, video):
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

    def do_all(self, device, video):
        time.sleep(.5)
        self.is_cuda_enabled()
        time.sleep(2.5)
        self.cpu_vs_gpu()
        time.sleep(2.5)
        self.fps_test(device, video)


def clear_terminal():
    pl = platform.system()
    if (pl == "Linux"):
        os.system("clear")
    elif (pl == "Windows"):
        os.system("cls")