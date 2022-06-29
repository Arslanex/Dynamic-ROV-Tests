from ThreadClasses import *
import cv2 as cv

def threadYolov3(src=0, yolo="320"):
    """
    3 Thread - Getting Video Feed
             - Showing Video Feed
             - Detection Function
    """
    video_getter = VideoGet(src).start()
    video_shower = VideoShow().start()
    object_detector = DetectObjects().start()
    arduino_com = ArduinoCom('com4', 9600).start()

    if (yolo == "320"):
        configFile = "yolov3-320.cfg"
        weightsFile = "yolov3-320.weights"
        inputSize = 320

    elif (yolo == "416"):
        configFile = "yolov3-416.cfg"
        weightsFile = "yolov3-416.weights"
        inputSize = 416

    elif (yolo == "tiny"):
        configFile = "yolov3-tiny.cfg"
        weightsFile = "yolov3-tiny.weights"
        inputSize = 416

    model = cv.dnn.readNetFromDarknet(configFile, weightsFile)
    dev = cv.cuda.getCudaEnabledDeviceCount()

    if (dev == 0):
        print("INFO :: CPU Kullanılıyor")
        model.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
        model.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

    elif (dev != 0):
        print("INFO :: GPU Kullanılıyor")
        model.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
        model.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA)

    layerNames = model.getLayerNames()
    outputLayerNames = [(layerNames[int(i) - 1]) for i in model.getUnconnectedOutLayers()]

    while True:
        if video_getter.stopped or video_shower.stopped or cv.waitKey(1) == ord("q") :
            video_shower.stop()
            video_getter.stop()
            object_detector.stop()
            arduino_com.stop()
            break
        frame = video_getter.frame
        blob = cv.dnn.blobFromImage(frame, 1 / 255, (inputSize, inputSize), [0, 0, 0], 1, crop=False)
        model.setInput(blob)
        outputLayers = model.forward(outputLayerNames)

        cv.line(frame, (300, 0), (300, 720), (255, 0, 255), 1)
        cv.line(frame, (980, 0), (980, 720), (255, 0, 255), 1)

        object_detector.frame = frame
        object_detector.outputs = outputLayers

        centerCoors = object_detector.centerCoor
        arduino_com.centerCoor = centerCoors

        frame = object_detector.frame
        video_shower.frame = frame

threadYolov3()