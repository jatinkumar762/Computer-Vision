import cv2
import numpy as np
import matplotlib.pyplot as plt

Images = []
for i in range(1,7):
    img = cv2.imread(str(i)+'.jpg')
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    row,col= gray.shape
    s = 1024/max(row,col)
    nrow = int(row*s)
    ncol = int(col*s)
    dim = (ncol, nrow)
    ngray = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    Images.append(ngray)

Keypoints = []
Descriptors = []

orb = cv2.ORB_create(nfeatures=500)
Keypoints.clear()
Descriptors.clear()
for i in range(len(Images)):
    kp,des = orb.compute(Images[i],None)
    Keypoints.append(kp)
    Descriptors.append(des)
print(len(Descriptors))






