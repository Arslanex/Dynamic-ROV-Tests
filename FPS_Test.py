import argparse
import time

import cv2
import numpy as np


def main(video, device):

    timers = {
        "full pipeline": [],
        "reading": [],
        "pre-process": [],
        "optical flow": [],
        "post-process": [],
    }

    cap = cv2.VideoCapture(video)
    fps = cap.get(cv2.CAP_PROP_FPS)
    num_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    ret, previous_frame = cap.read()
    if device == "cpu":
        if ret:
            frame = cv2.resize(previous_frame, (960, 540))
            previous_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
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
                frame = cv2.resize(frame, (960, 540))
                current_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                end_pre_time = time.time()
                timers["pre-process"].append(end_pre_time - start_pre_time)
                start_of = time.time()
                flow = cv2.calcOpticalFlowFarneback(
                    previous_frame, current_frame, None, 0.5, 5, 15, 3, 5, 1.2, 0,
                )
                end_of = time.time()
                timers["optical flow"].append(end_of - start_of)
                start_post_time = time.time()
                magnitude, angle = cv2.cartToPolar(
                    flow[..., 0], flow[..., 1], angleInDegrees=True,
                )

                hsv[..., 0] = angle * ((1 / 360.0) * (180 / 255.0))
                hsv[..., 2] = cv2.normalize(
                    magnitude, None, 0.0, 1.0, cv2.NORM_MINMAX, -1,
                )

                hsv_8u = np.uint8(hsv * 255.0)
                bgr = cv2.cvtColor(hsv_8u, cv2.COLOR_HSV2BGR)
                previous_frame = current_frame
                end_post_time = time.time()
                timers["post-process"].append(end_post_time - start_post_time)
                end_full_time = time.time()
                timers["full pipeline"].append(end_full_time - start_full_time)

                cv2.imshow("original", frame)
                cv2.imshow("result", bgr)
                k = cv2.waitKey(1)
                if k == 27:
                    break

    else:
        if ret:
            frame = cv2.resize(previous_frame, (960, 540))
            gpu_frame = cv2.cuda_GpuMat()
            gpu_frame.upload(frame)
            previous_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gpu_previous = cv2.cuda_GpuMat()
            gpu_previous.upload(previous_frame)
            gpu_hsv = cv2.cuda_GpuMat(gpu_frame.size(), cv2.CV_32FC3)
            gpu_hsv_8u = cv2.cuda_GpuMat(gpu_frame.size(), cv2.CV_8UC3)
            gpu_h = cv2.cuda_GpuMat(gpu_frame.size(), cv2.CV_32FC1)
            gpu_s = cv2.cuda_GpuMat(gpu_frame.size(), cv2.CV_32FC1)
            gpu_v = cv2.cuda_GpuMat(gpu_frame.size(), cv2.CV_32FC1)
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
                gpu_frame = cv2.cuda.resize(gpu_frame, (960, 540))
                gpu_current = cv2.cuda.cvtColor(gpu_frame, cv2.COLOR_BGR2GRAY)
                end_pre_time = time.time()
                timers["pre-process"].append(end_pre_time - start_pre_time)
                start_of = time.time()
                gpu_flow = cv2.cuda_FarnebackOpticalFlow.create(
                    5, 0.5, False, 15, 3, 5, 1.2, 0,
                )
                gpu_flow = cv2.cuda_FarnebackOpticalFlow.calc(
                    gpu_flow, gpu_previous, gpu_current, None,
                )

                end_of = time.time()
                timers["optical flow"].append(end_of - start_of)
                start_post_time = time.time()
                gpu_flow_x = cv2.cuda_GpuMat(gpu_flow.size(), cv2.CV_32FC1)
                gpu_flow_y = cv2.cuda_GpuMat(gpu_flow.size(), cv2.CV_32FC1)
                cv2.cuda.split(gpu_flow, [gpu_flow_x, gpu_flow_y])
                gpu_magnitude, gpu_angle = cv2.cuda.cartToPolar(
                    gpu_flow_x, gpu_flow_y, angleInDegrees=True,
                )

                gpu_v = cv2.cuda.normalize(gpu_magnitude, 0.0, 1.0, cv2.NORM_MINMAX, -1)
                angle = gpu_angle.download()
                angle *= (1 / 360.0) * (180 / 255.0)
                gpu_h.upload(angle)
                cv2.cuda.merge([gpu_h, gpu_s, gpu_v], gpu_hsv)
                gpu_hsv.convertTo(cv2.CV_8U, 255.0, gpu_hsv_8u, 0.0)
                gpu_bgr = cv2.cuda.cvtColor(gpu_hsv_8u, cv2.COLOR_HSV2BGR)
                frame = gpu_frame.download()
                bgr = gpu_bgr.download()
                gpu_previous = gpu_current
                end_post_time = time.time()
                timers["post-process"].append(end_post_time - start_post_time)
                end_full_time = time.time()
                timers["full pipeline"].append(end_full_time - start_full_time)
                cv2.imshow("original", frame)
                cv2.imshow("result", bgr)
                k = cv2.waitKey(1)
                if k == 27:
                    break

    cap.release()
    cv2.destroyAllWindows()

    print("Number of frames : ", num_frames)
    print("Elapsed time")
    for stage, seconds in timers.items():
        print("-", stage, ": {:0.3f} seconds".format(sum(seconds)))

    print("Default video FPS : {:0.3f}".format(fps))

    of_fps = (num_frames - 1) / sum(timers["optical flow"])
    print("Optical flow FPS : {:0.3f}".format(of_fps))

    full_fps = (num_frames - 1) / sum(timers["full pipeline"])
    print("Full pipeline FPS : {:0.3f}".format(full_fps))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="OpenCV CPU/GPU Comparison")
    parser.add_argument("--video", help="path to .mp4 video file", required=True, type=str)
    parser.add_argument(
        "--device",
        default="cpu",
        choices=["cpu", "gpu"],
        help="device to inference on",
    )

    args = parser.parse_args()
    video = args.video
    device = args.device

    print("Configuration")
    print("- device : ", device)
    print("- video file : ", video)

    main(video, device)