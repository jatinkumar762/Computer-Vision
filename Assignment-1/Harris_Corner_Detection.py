import cv2
import numpy as np 
import matplotlib.pyplot as plt

def sobel_filters(img):
    Kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], np.float32)
    Ky = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], np.float32)
    
    
    Ix = cv2.filter2D(img,-1,Kx)
    Iy = cv2.filter2D(img,-1,Ky)

    print(Ix.shape)
    print(Iy.shape)

    #Ixx =  cv2.filter2D(Ix,-1,Ix)
    #Iyy =  cv2.filter2D(Iy,-1,Iy)
    #Ixy =  cv2.filter2D(Ix,-1,Iy)
    Ixx = np.square(Ix)
    Iyy = np.square(Iy)
    Ixy = np.dot(Ix,Iy)

    Ixx = Ixx / Ixx.max() * 255
    Iyy = Iyy / Iyy.max() * 255
    Ixy = Ixy / Ixy.max() * 255

    return (Ixx, Iyy, Ixy)


image = cv2.imread('checkerboard.png')
plt.axis("off")
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.show()

image_copy = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
plt.axis("off")
plt.imshow(image_copy,cmap='gray')
plt.show()

blur=cv2.GaussianBlur(image_copy,(5,5),0)
plt.axis("off")
plt.imshow(blur,cmap='gray')
plt.show() 


Ixx, Iyy, Ixy = sobel_filters(blur)

b_Ixx = cv2.GaussianBlur(Ixx,(5,5),0)
b_Iyy = cv2.GaussianBlur(Iyy,(5,5),0)
b_Ixy = cv2.GaussianBlur(Ixy,(5,5),0)

k=0.04
detA = b_Ixx * b_Iyy - b_Ixy ** 2
traceA = b_Ixx + b_Iyy
harris_response = detA - k * traceA ** 2

harris_response = cv2.dilate(harris_response,None)
#print(harris_response)
#print(harris_response[harris_response>0])

image[harris_response>0.01*harris_response.max()]=[0,0,255]
plt.axis("off")
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.show()





