import cv2
import numpy as np 
import matplotlib.pyplot as plt

image = cv2.imread('checkerboard.png')
plt.axis("off")
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.show()

image_copy = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
plt.axis("off")
plt.imshow(image_copy,cmap='gray')
plt.show()

image_copy = np.float32(image_copy)
dst = cv2.cornerHarris(image_copy,2,3,0.04)
print(dst)
dst = cv2.dilate(dst,None)
plt.axis("off")
plt.imshow(dst, cmap='gray')
plt.show()

image[dst>0.01*dst.max()]=[0,255,0]
plt.axis("off")
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.show()





