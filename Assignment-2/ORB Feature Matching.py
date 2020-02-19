import cv2
import numpy as np
import matplotlib.pyplot as plt

#store all resized images
Images = []

#Resize all the images
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

#arrays to store keypoints and descriptors
Keypoints = []
Descriptors = []

#initialize orb object
orb = cv2.ORB_create(nfeatures=500)
Keypoints.clear()
Descriptors.clear()
min_row = 999

#store descriptor and keyoints of all images
for i in range(len(Images)):
    kp,des = orb.detectAndCompute(Images[i],None)
    Keypoints.append(kp)
    Descriptors.append(des)
    if des.shape[0] < min_row:
    	min_row = des.shape[0]


r = min_row
k=10 # top-k matches of the features
dict_i = {}
accuracy = 0

totq_imgs = 36
for key_image in range(0,totq_imgs):  #pick image one by one
    for i in range(0,36):             #other images for key image
        if i == key_image:
            pass
        else:
            dist = []
            dist.clear()
            for m in range(Descriptors[key_image].shape[0]):
                minVal = 9999
                for n in range(Descriptors[i].shape[0]):
                    cur_val = np.linalg.norm(Descriptors[key_image][m]-Descriptors[i][n])
                    if cur_val<minVal:
                        minVal = cur_val
                dist.append(minVal)
            dist.sort() #sort the distances odf image
            avg = np.average(dist[:k])  #calculate avg
            dict_i[i]=avg

    #sort the images according to avg distance
    sorted_d = np.asarray(sorted(dict_i.items(), key=lambda x: x[1]))
    match_index = sorted_d[:5,:1].astype(int).tolist()

    key_gp = (key_image+1)//6  #calculate the gpof key image
    if (key_image+1)%6 !=0:
        key_gp+=1

    count=0
    for mi in match_index:  #calculate the index of matched images
        mi_gp = (mi[0]+1)//6
        if (mi[0]+1)%6 !=0:
            mi_gp+=1
        if mi_gp == key_gp:
            count+=1

    if count == 5:    #calculate accuracy
        accuracy+=100
    else:
        accuracy+=(count/5)*100

print('Avg Accuracy: ',accuracy/totq_imgs)






