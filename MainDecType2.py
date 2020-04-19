import numpy as np
import cv2
import keras as k
#import Tensorflow as tf
from keras.models import load_model
import keras.backend as K

cap = cv2.VideoCapture(0)

def customLoss(true, pred):
    return K.sum((true-pred)**2, axis = 1)

model = load_model('model4_4.h5', custom_objects={"customLoss" : customLoss})

target_size = 224

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")
print("starting")
while True:
    ret, frame = cap.read()
    ori_Frame = frame
    x_scale = target_size / frame.shape[0]
    y_scale = target_size / frame.shape[1]

    resizedImg = cv2.resize(frame, (target_size, target_size), interpolation=cv2.INTER_AREA)

    resizedImg = resizedImg/255 - .5
    hand_Pos = model.predict(resizedImg.reshape(1, target_size, target_size, 3))

    frame = hand_Pos.reshape(28, 28, 1)
    print(hand_Pos)
    print("showing")
    cv2.imshow('Input', frame)

    c = cv2.waitKey(1)
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()