# -*- coding: utf-8 -*-
"""HandDetectorTrainer.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1475Mmrf1U6PRFuyetNI-rg0NsA6mgs1T
"""

!wget http://www.robots.ox.ac.uk/~vgg/data/hands/downloads/hand_dataset.tar.gz
!tar -xf hand_dataset.tar.gz
!rm hand_dataset.tar.gz

!ls

import numpy as np
import cv2
import os
from scipy.io import loadmat
from tqdm import tqdm
import tensorflow as tf
import keras as k

from keras.models import load_model
from sklearn.datasets import load_files   
from keras.utils import np_utils
from keras import applications
from keras import optimizers
from keras.models import Sequential,Model,load_model
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D,GlobalAveragePooling2D
from keras.callbacks import TensorBoard,ReduceLROnPlateau,ModelCheckpoint
from skimage.util import random_noise

path_to_annot = "hand_dataset/training_dataset/training_data/annotations/"
path_to_img = "hand_dataset/training_dataset/training_data/images/"

target_size = 224

out_target_size = 28

y = []
X = []

an = loadmat(path_to_annot + 'VOC2010_1006.mat')
print(an.keys())
print(an['boxes'].shape)
print(an['boxes'][0][0], end = "\n############\n")
print(an['boxes'][0][0][0][0][1][0])



#STEP 1 : Getting the DATA
#Load the annotations into a python list, while also converting the annotations from a .mat to a python-friendly type
X = [] #just to clear the previous data of x
y = [] #just to clear the previous data of y
print("Loading Position Data of one hand")

for root, dirs, files in os.walk(path_to_annot):
    for file in tqdm(files):
        if ".mat" in file:
            #getting the annotations and recording the points
            annots = loadmat(path_to_annot + file)['boxes'][0] #For simplicity and use-case only one 
                                                                        #hand will be looked for
            #getting the image and then scaling it to a target_size by target_size img
            img = cv2.imread(path_to_img + file.strip(".mat") + ".jpg")
            noise_img = random_noise(img, mode='s&p',amount=0.3)
            orignalShape = img.shape
            img = cv2.resize(img, (target_size,target_size), interpolation = cv2.INTER_AREA)
            noise_img = cv2.resize(noise_img, (target_size,target_size), interpolation = cv2.INTER_AREA)
            img = img/255 - .5
            noise_img = noise_img/255 -.5
            cv2.imwrite('test.png',img)

            outMask = np.zeros(orignalShape, dtype = "uint8")
            for annot in annots:
                pt1 = np.flip(annot[0][0][0])
                pt2 = np.flip(annot[0][0][1])
                pt3 = np.flip(annot[0][0][2])
                pt4 = np.flip(annot[0][0][3])
                pts = np.array([pt1[0],pt2[0],pt3[0],pt4[0]], np.int32)
                pts = pts.reshape((-1,1,2))
                outMask = cv2.fillPoly(outMask,[pts], (255,255,255))
            outMask = cv2.cvtColor(outMask, cv2.COLOR_BGR2GRAY)
            outMask = cv2.resize(outMask, (out_target_size,out_target_size), interpolation = cv2.INTER_AREA)
            cv2.imwrite('testOut.png',outMask)
            X.append(img)
            X.append(noise_img)
            y.append(outMask)
            y.append(outMask)

#Load the image data and resize it to a 200 by 200 image
X = np.array(X)
y = np.array(y).reshape(-1, out_target_size, out_target_size, 1)

#STEP 3: print sizes of Image and Bounding-box datasets
print(X.shape)
print(y.shape)

#X = X[0:3000]
#y = y[0:3000]

from keras.applications.vgg16 import VGG16
from keras.applications.mobilenet import MobileNet
#If imagenet weights are being loaded, 
#input must have a static square shape (one of (128, 128), (160, 160), (192, 192), or (224, 224))
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(target_size, target_size, 3))
"""base_model = MobileNet(weights='imagenet', include_top=False, input_shape=(target_size, target_size, 3))"""
#x = GlobalAveragePooling2D()(base_model.layers[-50].output)
x = Conv2D(1, (1, 1), activation="linear")(base_model.layers[-6].output)
model = Model(inputs = base_model.input, outputs = x)

print(model.summary())

from keras.optimizers import SGD, Adam
import keras.backend as K

def customLoss(true, pred):
    return K.sum((true-pred)**2, axis = 1)

model.compile(optimizer= "adam", loss = customLoss, metrics=['accuracy'])#The loss is meant for results above 1

model.fit(X, y, epochs = 50, batch_size = 30, shuffle = True, validation_split= .01, use_multiprocessing=True, verbose = 1)
model.save("model4_other.h5")

model.save("model4_other.h5")



