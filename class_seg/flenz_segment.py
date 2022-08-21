import numpy as np
from glob import glob
from PIL import Image
from matplotlib import pyplot as plt
from felzenszwalb_segmentation import segment
import cv2
import random
import time
import os

#C:\aa\bridge_intellegence\AR_ND_UT\1120\00a5f78c-caec-40db-adcc-d7a7f028797f_1628032453222thumb.jpg
'''
image = np.array(Image.open(r'C:\aa\bridge_intellegence\AR_ND_UT\1120\00a5f78c-caec-40db-adcc-d7a7f028797f_1628032453222thumb.jpg'))
print(image.shape)
segmented_image = segment(image, 0.2, 400, 100)

fig = plt.figure(figsize=(12, 12))
a = fig.add_subplot(1, 2, 1)
plt.imshow(image)
a = fig.add_subplot(1, 2, 2)
plt.imshow(segmented_image.astype(np.uint8))
plt.show()
'''

#%matplotlib inline
path = "C:\\aa\\bridge_intellegence\\ROI_dataset"
files = os.listdir(path)   


for j in range(0, len(files)):
    if j % 15 == 0:
        print("count", j)
    i = files[j]
    img_path = str(path)+"\\"+str(i)
    # load the input image
    #image = cv2.imread(img_path)
    #print(image.shape)
    # input image
    image = np.array(Image.open(img_path))
    #print(image.shape)
    segmented_image = segment(image, 0.2, 400, 100)
    fig = plt.figure()
    a = fig.add_subplot(1, 2, 1)
    a.set_title('Input')
    plt.imshow(image)
    a = fig.add_subplot(1, 2, 2)
    a.set_title('Segmented Map')
    plt.imshow(segmented_image.astype(np.uint8))
    #plt.show()
    plt.savefig("C:\\aa\\bridge_intellegence\\initial_trans_codes\\fel_segmentation\\" + str(i))
    plt.close()
    #cv2.imwrite("C:\\aa\\bridge_intellegence\\fel_segmentation\\" + str(i), segmented_image.astype(np.uint8))
    #key = cv2.waitKey(0) & 0xFF
    # if the `q` key was pressed, break from the loop
    #if key == ord("q"):
        #break
