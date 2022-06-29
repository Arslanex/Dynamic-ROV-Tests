from threading import Thread
import numpy as np
import cv2 as cv
import serial

class VideoGet:
    def __init__(self, src=0):
        self.cap = cv.VideoCapture(src)
        self.cap.set(3, 1280)
        self.cap.set(4, 720)
        self.ret, self.frame = self.cap.read()
        self.stopped = False

    def start(self):
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        while not self.stopped:
            if not self.ret:
                self.stop()
            else:
                (self.grabbed, self.frame) = self.cap.read()

    def stop(self):
        self.stopped = True

class VideoShow:
    def __init__(self, frame=None):
        self.frame = frame
        self.stopped = False

    def start(self):
        Thread(target=self.show, args=()).start()
        return self

    def show(self):
        while not self.stopped:
            if self.frame is not None:
                cv.imshow("Video", self.frame)
            if cv.waitKey(1) == ord("q"):
                self.stopped = True

    def stop(self):
        self.stopped = True

class DetectObjects:
    def __init__(self, outputs=None, frame=None):
        self.outputs = outputs
        self.frame = frame
        self.stopped = False
        self.centerCoor = []
        self.confVal = []

    def start(self):
        Thread(target=self.detection, args=()).start()
        return self

    def detection(self):
        while not self.stopped:
            if self.outputs is not None and self.frame is not None:
                imgHeight, imgWidth = self.frame.shape[:2]

                boundingBoxes = []
                objectsIds = []
                confidenceRates = []

                for output in self.outputs:
                    for detection in output:

                        detectionScores = detection[5:]
                        objectId = np.argmax(detectionScores)
                        confidence = detectionScores[objectId]

                        if confidence > 0.9:
                            w, h = int(detection[2] * imgWidth), int(detection[3] * imgHeight)
                            x, y = int((detection[0] * imgWidth) - w / 2), int((detection[1] * imgHeight) - h / 2)

                            boundingBoxes.append([x, y, w, h])
                            objectsIds.append(objectId)
                            confidenceRates.append(float(confidence))

                indexes = cv.dnn.NMSBoxes(boundingBoxes, confidenceRates, .7, .3)

                self.centerCoor = []
                self.confVal = []

                for i in indexes:
                    box = boundingBoxes[int(i)]
                    x, y, w, h = box[0], box[1], box[2], box[3]
                    cx, cy = int(x + w / 2), int(y + h / 2)
                    cv.rectangle(self.frame, (x, y), (x + w, y + h), (255, 0, 255), 2)
                    cv.circle(self.frame, (cx, cy), 5, (0, 0, 255), 3)
                    self.centerCoor.append([cx, cy])
                    self.confVal.append(confidenceRates[int(i)])

    def stop(self):
        self.stopped = True

class ArduinoCom:
    def __init__(self, com, baund, centerCoor=[]):
        self.arduino = serial.Serial(com, baund)
        self.arduino.timeout = 1
        self.centerCoor = centerCoor
        self.stopped = False

    def send(self):
        while not self.stopped:
            self.arduino.readline().decode('ascii')
            i = "M"
            if self.centerCoor != []:
                if (self.centerCoor[0][0] < 300):
                    i = "R"
                elif (self.centerCoor[0][0] > 980):
                    i = "L"

            self.arduino.write(i.encode())

    def start(self):
        Thread(target=self.send, args=()).start()
        return self

    def stop(self):
        self.stopped = True
        self.arduino.close()
