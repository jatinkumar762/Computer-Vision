import cv2
import numpy as np
import matplotlib.pyplot as plt

Images = []

for i in range(1,37):
    img = cv2.imread('Images\\'+str(i)+'.jpg')
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

sift = cv2.xfeatures2d.SIFT_create(500)
Keypoints.clear()
Descriptors.clear()
min_row = 999
for i in range(len(Images)):
    kp,des = sift.detectAndCompute(Images[i],None)
    Keypoints.append(kp)
    Descriptors.append(des)
    if des.shape[0] < min_row:
    	min_row = des.shape[0]

r = min_row
k=10
dict_i = {}
accuracy = 0

for key_image in range(0,3):
    for i in range(0,36):
        if i == key_image:
            pass
        else:
            dist = []
            dist.clear()
            for m in range(Descriptors[key_image].shape[0]):
                minVal = 9999
                for n in range(Descriptors[i].shape[0]):
                    if np.linalg.norm(Descriptors[key_image][m]-Descriptors[i][n])<minVal:
                        minVal = np.linalg.norm(Descriptors[key_image][m]-Descriptors[i][n])
                dist.append(minVal)
            dist.sort() 
            avg = np.average(dist[:k])
            dict_i[i]=avg

    sorted_d = np.asarray(sorted(dict_i.items(), key=lambda x: x[1]))
    match_index = sorted_d[:5,:1].astype(int).tolist()

    key_gp = (key_image+1)//6
    if (key_image+1)%6 !=0:
        key_gp+=1

    count=0
    for mi in match_index:
        mi_gp = (mi[0]+1)//6
        if (mi[0]+1)%6 !=0:
            mi_gp+=1
        if mi_gp == key_gp:
            count+=1

    if count == 5:
        accuracy+=100
    else:
        accuracy+=(count/5)*100

print(accuracy/3)

#print(dict_i)
#sorted_d = np.asarray(sorted(dict_i.items(), key=lambda x: x[1]))
#print(sorted_d[:5,:1].astype(int).tolist())
# match_index = sorted_d[:5,:1].astype(int).tolist()

# key_gp = (key_image+1)//6
# if (key_image+1)%6 !=0:
#     key_gp+=1

# count=0
# for mi in match_index:
#     mi_gp = (mi[0]+1)//6
#     if (mi[0]+1)%6 !=0:
#         mi_gp+=1
#     if mi_gp == key_gp:
#         count+=1

# if count == 5:
#     print(100)
# else:
#     print((count/5)*100)



