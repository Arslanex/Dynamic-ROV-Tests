import cv2 as cv
import numpy as np
import serial

### CONFIGRATION
cap = cv.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

serialcomm = serial.Serial('com4', 9600)
serialcomm.timeout = 1

config = "../Files/yolo_config/yolov3-320.cfg"
weights = "../Files/yolo_weights/yolov3-320.weights"
nameFile = "../Files/name_files/coco.names"

MNSThreshold = 0.2
confidenceThreshold = 0.5

inputSize = 320
color = (255, 0, 255)
font = cv.FONT_HERSHEY_COMPLEX_SMALL

### SET-UP
nameOfClasses = []
with open(nameFile, "r") as f:
    nameOfClasses = [line.strip() for line in f.readlines()]

model = cv.dnn.readNetFromDarknet(config, weights)

model.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
model.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA)

### DETECTION FUNCTION
def object_detection_with_MNS(outputs, img, mode = 0):
    height, width, channel = img.shape

    boundingBoxes = []
    objectsIds = []
    confidenceRates = []

    for output in outputs:
        for detection in output:

            detectionScores = detection[5:]
            objectId = np.argmax(detectionScores)
            confidence = detectionScores[objectId]

            if confidence > 0.7:
                w, h = int(detection[2] * width), int(detection[3] * height)
                x, y = int((detection[0] * width) - w / 2), int((detection[1] * height) - h / 2)

                boundingBoxes.append([x, y, w, h])
                objectsIds.append(objectId)
                confidenceRates.append(float(confidence))

        indexes = cv.dnn.NMSBoxes(boundingBoxes, confidenceRates, confidenceThreshold, MNSThreshold)

        if mode == 0:
            for i in indexes:
                box = boundingBoxes[i]
                x, y, w, h = box[0], box[1], box[2], box[3]
                cv.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)
                cv.putText(img, "{}, %{}".format(nameOfClasses[objectsIds[i]].upper(), int(confidenceRates[i] * 100)),
                           (x, y - 10), font, 2, color, 3)

        elif mode == 1:
            for i in indexes:
                box = boundingBoxes[i]
                x, y, w, h = box[0], box[1], box[2], box[3]
                cx, cy = int(x+w/2), int(y+h/2)
                cv.circle(img, (cx, cy), 5 , (0,0,255), 3)

        elif mode == 2:
            centerCoor = []
            confVal = []
            for i in indexes:
                box = boundingBoxes[i]
                x, y, w, h = box[0], box[1], box[2], box[3]
                cx, cy = int(x + w / 2), int(y + h / 2)
                centerCoor.append([cx, cy])
                confVal.append(confidenceRates[i])
    if mode == 2:
        val = zip(centerCoor, confVal)
        return centerCoor, confVal, list(val)
    else:
        return None, None, None

### SEND and RECIVE DATA
while True:
    ret, frame = cap.read()

    frame = cv.flip(frame, -1)
    blob = cv.dnn.blobFromImage(frame, 1 / 255, (inputSize, inputSize), [0, 0, 0], 1, crop=False)

    model.setInput(blob)
    layerNames = model.getLayerNames()
    outputLayerNames = [(layerNames[i - 1]) for i in model.getUnconnectedOutLayers()]
    outputs =  model.forward(outputLayerNames)

    a, b, c = object_detection_with_MNS(outputs, frame, 2)
    if a != []:
        cv.circle(frame, (a[0]), 5, (255, 0, 0), -1)
        if(a[0][0] < 300):
            serialcomm.write("R".encode())
        elif(a[0][0] > 980):
            serialcomm.write("L".encode())
        else:
            serialcomm.write("90".encode())

    print(serialcomm.readline().decode('ascii'))
    cv.line(frame, (300, 0), (300, 720), (255,0,255), 1)
    cv.line(frame, (980, 0), (980, 720), (255,0,255), 1)
    cv.imshow("Frame", frame)
    if cv.waitKey(1) == ord("q"):
        break

cap.release()
cv.destroyAllWindows()