import cv2
import numpy as np
import os
 
#The line below is necessary to show Matplotlib's plots inside a Jupyter Notebook
#%matplotlib inline
 
from matplotlib import pyplot as plt

#path = "C:\\aa\\bridge_intellegence\\B\\6000"
path = "C:\\aa\\bridge_intellegence\\ROI_dataset"
files = os.listdir(path)   


for j in range(0,len(files)):
    i = files[j]
    img_path = str(path)+"\\"+str(i)
    reddress = cv2.imread(img_path)

    reddress_hsv = cv2.cvtColor(reddress, cv2.COLOR_BGR2HSV)
    
    # Remember that in HSV space, Hue is color from 0..180. Red 320-360, and 0 - 30.
    # We keep Saturation and Value within a wide range but note not to go too low or we start getting black/gray
    lower_green = np.array([30,40,20])
    upper_green = np.array([255,255,255])

    lower_black = np.array([0,0,0])
    upper_black = np.array([170,150,50])
    
    # Using inRange method, to create a mask
    #mask = cv2.inRange(reddress_hsv, lower_green, upper_green)
    mask = cv2.inRange(reddress_hsv, lower_black, upper_black)
    mask_inv = mask
    mask_inv = mask
    mask_inv[mask_inv==255] = 10
    mask_inv[mask_inv==0] = 255
    mask_inv[mask_inv==10] = 0
    reddress_gray = cv2.cvtColor(reddress,cv2.COLOR_BGR2GRAY)
    reddress_gray = cv2.cvtColor(reddress_gray,cv2.COLOR_GRAY2BGR)
    forest = cv2.bitwise_and(reddress_gray, reddress_gray, mask=mask)
    lady = cv2.bitwise_and(reddress,reddress, mask= mask_inv)
    lady = lady #+ 0.001*forest
    cv2.imwrite("C:\\aa\\bridge_intellegence\\hsv_transform\\" + str(i), lady)
    
    #cv2.imshow("Output", lady)
    #cv2.waitKey(0)