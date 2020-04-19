import numpy as np
import cv2
from keras.models import load_model
import keras.backend as K
import math
from collections import deque

class Locate:
    def __init__(self, camera_instance=cv2.VideoCapture(0), model_path="model4_4.h5"):
        self.pastFaceScores = deque(5 * [1000], 15)

        self.target_size = 224
        print("Instantiating Camera")
        self.cam = camera_instance
        self.camSize = []
        print("Instantiating Hand Model")
        self.HandModel = load_model('model4_4.h5',
                                    custom_objects={"customLoss": self.customLoss})
        print("Instantiating Face Casade")
        self.face_Cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
        print("Done Instantiating")

    def getpicfromCamera(self):
        ret, frame = self.cam.read()
        self.camSize = frame.shape
        return frame

    def getfacecoordinates(self, frame=None):
        """
        This method returns the coordinates of faces as a double ranging from 0 to 1
        :return:
        """
        if frame is None:
            frame = self.getpicfromCamera()

        scale = .6
        frame = cv2.resize(frame, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        frameSize = gray.shape
        #print(frameSize)
        faces = self.face_Cascade.detectMultiScale(gray, 1.05, 5)

        if len(faces) == 0: #If no face is found
            return faces

        face_sizes = faces[:,2] * faces[:, 3]
        biggestFaceIndex = np.argmax(face_sizes)
        faces = faces[biggestFaceIndex].reshape(1, 4) #Prunes the face list down to the biggest face

        faces = faces.astype(dtype = np.float)
        for x in range(0, len(faces)): #TODO : Change the float creation into numpy array operation
            faces[x][0] /= frameSize[1]
            faces[x][1] /= frameSize[0]
            faces[x][2] /= frameSize[1]
            faces[x][3] /= frameSize[0]
        return faces

    def customLoss(self, true, pred):
        return K.sum((true - pred) ** 2, axis=1)

    def gethandProbMap(self, frame = None):
        if frame is None:
            frame = self.getpicfromCamera()
        frame = cv2.resize(frame, (self.target_size, self.target_size), interpolation=cv2.INTER_AREA)
        frame = frame / 255 - .5
        hand_Pos = self.HandModel.predict(frame.reshape(1, self.target_size, self.target_size, 3))
        frame = hand_Pos.reshape(28, 28, 1)

        return frame

    def getOverLapDiagnostic(self, handMap, faceCoordinates, threshold_boost=2.1):
        if len(faceCoordinates) == 0:
            return False
        for (x, y, w, h) in faceCoordinates: # The coordinates of the face box has to be reflected across an axis going vertically down the center of the image. The coordinates also have to be converted into a 14*14 index
            handMapX = int(x * handMap.shape[0])
            handMapY = int(y * handMap.shape[1])
            handMapW = math.ceil(w * handMap.shape[0])
            handMapH = math.ceil(h * handMap.shape[1])

            handMapX2 = min(handMap.shape[0], handMapX + handMapW)
            handMapY2 = min(handMap.shape[1], handMapY + handMapH)


            #print((handMapX, handMapX2))
            subSection = handMap[handMapX: handMapX2, handMapY: handMapY2]
            total = np.sum(subSection)
            total = total/(handMapW * handMapH)
            handMap = cv2.cvtColor(handMap,cv2.COLOR_GRAY2RGB)
            handMap = cv2.rectangle(handMap, (handMapX, handMapY), (handMapX2, handMapY2), (255, 255, 0), 1)
            handMap = cv2.resize(handMap, (400, 400), interpolation=cv2.INTER_AREA)
            #print(total)
            pastScoresAvg = np.mean(np.array(self.pastFaceScores)) + threshold_boost * np.std(np.array(self.pastFaceScores))
            self.pastFaceScores.appendleft(total)
            if(total >= pastScoresAvg * threshold_boost):
                handMap = cv2.putText(handMap,"Detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.imshow("finalOut", handMap)
                return True
            handMap = cv2.putText(handMap, "Not Detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
                                  cv2.LINE_AA)
            cv2.imshow("finalOut", handMap)
        return False

    def close(self):
        cv2.release()

    def getOverLap(self, handMap, faceCoordinates, threshold_boost=2.1):
        if len(faceCoordinates) == 0:
            return False
        for (x, y, w, h) in faceCoordinates: # The coordinates of the face box has to be reflected across an axis going vertically down the center of the image. The coordinates also have to be converted into a 14*14 index
            handMapX = int(x * handMap.shape[0])
            handMapY = int(y * handMap.shape[1])
            handMapW = math.ceil(w * handMap.shape[0])
            handMapH = math.ceil(h * handMap.shape[1])

            handMapX2 = min(handMap.shape[0], handMapX + handMapW)
            handMapY2 = min(handMap.shape[1], handMapY + handMapH)


            #print((handMapX, handMapX2))
            subSection = handMap[handMapX: handMapX2, handMapY: handMapY2]
            total = np.sum(subSection)
            total = total/(handMapW * handMapH)
            #print(total)
            pastScoresAvg = np.mean(np.array(self.pastFaceScores)) + threshold_boost * np.std(np.array(self.pastFaceScores))
            self.pastFaceScores.appendleft(total)
            if(total >= pastScoresAvg * threshold_boost):
                print("Hand has touched face -> 1")
                return True
        print("Hand hasn't touched face -> 0")
        return False