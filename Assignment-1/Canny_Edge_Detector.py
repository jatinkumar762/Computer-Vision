import cv2
import numpy as np
import matplotlib.pyplot as plt

def filter_sobel(image):
    Sx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], np.float32)
    Sy = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], np.float32)
    
    Ix = cv2.filter2D(img,-1,Sx)
    Iy = cv2.filter2D(img,-1,Sy)

    M = np.hypot(Ix, Iy)
    M = M / M.max() * 255
    theta = np.arctan2(Iy, Ix)
    
    return (M, theta) 


def Non_Maximal_Suppression(image, D):
    Row, Col = image.shape
    Z = np.zeros((Row,Col), dtype=np.int32)
    angle = D * 180. / np.pi
    angle[angle < 0] += 180

    
    for i in range(1,Row-1):
        for j in range(1,Col-1):
            try:
                q = 255
                r = 255
                
               #angle 0
                if (0 <= angle[i,j] < 22.5) or (157.5 <= angle[i,j] <= 180):
                    q = image[i, j+1]
                    r = image[i, j-1]
                #angle 45
                elif (22.5 <= angle[i,j] < 67.5):
                    q = image[i+1, j-1]
                    r = image[i-1, j+1]
                #angle 90
                elif (67.5 <= angle[i,j] < 112.5):
                    q = image[i+1, j]
                    r = image[i-1, j]
                #angle 135
                elif (112.5 <= angle[i,j] < 157.5):
                    q = image[i-1, j-1]
                    r = image[i+1, j+1]

                if (image[i,j] >= q) and (image[i,j] >= r):
                    Z[i,j] = image[i,j]
                else:
                    Z[i,j] = 0

            except IndexError as e:
                pass
    
    return Z

#identify strong weak and non relevamt pixels
def threshold(image, lowThRatio=0.05, highThRatio=0.09):
    
    highTh = image.max() * highThRatio;
    lowTh = highTh * lowThRatio;
    
    M, N = image.shape
    res = np.zeros((M,N), dtype=np.int32)
    
    weak = np.int32(100)
    strong = np.int32(200)

    x_strong, y_strong = np.where(image >= highTh)
    x_zeros, y_zeros = np.where(image < lowTh)
    
    x_weak, y_weak = np.where((image <= highTh) & (image >= lowTh))
    
    res[x_strong, y_strong] = strong
    res[x_weak, y_weak] = weak
    
    return (res, weak, strong)

def hysteresis(image, weak, strong=200):
    Row, Col = image.shape  
    for i in range(1, Row-1):
        for j in range(1, Col-1):
            if (image[i,j] == weak):
                try:
                    if ((image[i+1, j-1] == strong) or (image[i+1, j] == strong) or (image[i+1, j+1] == strong)
                        or (image[i, j-1] == strong) or (image[i, j+1] == strong)
                        or (image[i-1, j-1] == strong) or (image[i-1, j] == strong) or (image[i-1, j+1] == strong)):
                        image[i, j] = strong
                    else:
                        image[i, j] = 0
                except IndexError as e:
                    pass
    return image



img=cv2.imread('flower.jpg',0)
cv2.imshow('Flower', img) 
cv2.waitKey(0) 
cv2.destroyAllWindows() 


blur=cv2.GaussianBlur(img,(5,5),0)
cv2.imshow('Blurred Image', blur) 
cv2.waitKey(0) 
cv2.destroyAllWindows() 

G,theta = filter_sobel(img)
plt.axis("off")
plt.imshow(np.rint(G).astype(int),cmap = 'gray')
plt.show()

Z = Non_Maximal_Suppression(G,theta)
plt.axis("off")
plt.imshow(Z,cmap = 'gray')
plt.show()


res, weak, strong = threshold(Z)
plt.axis("off")
plt.imshow(res,cmap = 'gray')
plt.show()


eimg = hysteresis(res, weak)
plt.axis("off")
plt.imshow(eimg,cmap = 'gray')
plt.show()



edges = cv2.Canny(np.uint8(img),100,200)

plt.subplot(121),plt.imshow(img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
plt.show()