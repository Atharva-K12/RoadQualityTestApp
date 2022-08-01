from turtle import color
import numpy as np
from glob import glob
from PIL import Image
from matplotlib import pyplot as plt
import cv2
import random
import time
import os
import skimage.segmentation

#%matplotlib inline
path = "C:\\aa\\bridge_intellegence\\ROI_dataset"
files = os.listdir(path)   
treshold = 0.5
#img_path = r'C:\aa\bridge_intellegence\AR_ND_UT\1120\00a5f78c-caec-40db-adcc-d7a7f028797f_1628032453222thumb.jpg'
def NMS(boxes, image_shape, overlapThresh = 0.5):
    #return an empty list, if no boxes given
    if len(boxes) == 0:
        return []
    x1 = boxes[:, 0]  # x coordinate of the top-left corner
    y1 = boxes[:, 1]  # y coordinate of the top-left corner
    x2 = boxes[:, 2]  # x coordinate of the bottom-right corner
    y2 = boxes[:, 3]  # y coordinate of the bottom-right corner
    # compute the area of the bounding boxes and sort the bounding
    # boxes by the bottom-right y-coordinate of the bounding box
    areas = (x2 - x1 + image_shape[1]) * (y2 - y1 + image_shape[0]) # We have a least a box of one pixel, therefore the +1
    indices = np.arange(len(x1))
    for i,box in enumerate(boxes):
        temp_indices = indices[indices!=i]
        xx1 = np.maximum(box[0], boxes[temp_indices,0])
        yy1 = np.maximum(box[1], boxes[temp_indices,1])
        xx2 = np.minimum(box[2], boxes[temp_indices,2])
        yy2 = np.minimum(box[3], boxes[temp_indices,3])
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)
        # compute the ratio of overlap
        overlap = (w * h) / areas[temp_indices]
        if np.any(overlap) > overlapThresh:
            indices = indices[indices != i]
    return boxes[indices].astype(int)


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
    segmented_image = skimage.segmentation.felzenszwalb(image, scale=100, sigma=0.5, min_size= min(image.shape[0], image.shape[1]))
    #segmented_image = cv2.adaptiveThreshold(segmented_image.astype(np.uint8),255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
           #cv2.THRESH_BINARY,11,2)
    #noise_img_grey = cv2.cvtColor(segmented_image.astype(np.uint8), cv2.COLOR_BGR2GRAY)
    rect, segmented_image = cv2.threshold(segmented_image.astype(np.uint8),0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
           #cv2.THRESH_BINARY,11,2)
    
    
    #segmented_image = segmented_image.reshape(segmented_image.shape[0], segmented_image.shape[1], -1)
    segmented_image =  cv2.cvtColor(segmented_image,cv2.COLOR_GRAY2RGB)
    #print(segmented_image.shape)
    ss = cv2.ximgproc.segmentation.createSelectiveSearchSegmentation()
    ss.setBaseImage(segmented_image)
    #method = 'fast'
    method = 'quality'

    if method == "fast":
        #print("[INFO] using *fast* selective search")
        ss.switchToSelectiveSearchFast()
    # otherwise we are using the *slower* but *more accurate* version
    else:
        #print("[INFO] using *quality* selective search")
        ss.switchToSelectiveSearchQuality()

    # check to see if we are using the *fast* but *less accurate* version
    # run selective search on the input image
    start = time.time()
    rects = ss.process()
    end = time.time()
    # show how along selective search took to run along with the total
    # number of returned region proposals
    #print("[INFO] selective search took {:.4f} seconds".format(end - start))
    # loop over the region proposals in chunks (so we can better
    # visualize them
    rects = NMS(rects, image.shape, 0.5)                                   ######## for nms
    for m in range(0, len(rects)):   ####change parameters to 1
        #print("m", m)
        # clone the original image so we can draw on it
        output = image.copy()
        # loop over the current subset of region proposals
        for (x, y, w, h) in rects[m:m + 10]:                         #######test0 5
            # draw the region proposal bounding box on the image
            #color = [random.randint(0, 255) for j in range(0, 3)]
            color =(255,0,0)
            cv2.rectangle(output, (x, y), (x + w, y + h), color, 4)
        # show the output image
        #cv2.imshow("Output", output)
        #cv2.imwrite("C:\\aa\\bridge_intellegence\\selective_search\\" + str(i), output)

    fig = plt.figure()
    a = fig.add_subplot(1, 3, 1)
    a.set_title('Input')
    plt.imshow(image)
    a = fig.add_subplot(1, 3, 2)
    a.set_title('Segmented Map')
    plt.imshow(segmented_image)
    a = fig.add_subplot(1, 3, 3)
    a.set_title('Output')
    plt.imshow(output)
    #plt.show()
    plt.savefig("C:\\aa\\bridge_intellegence\\initial_trans_codes\\seg_depth\\" + str(i))
    plt.close()
    #cv2.imwrite("C:\\aa\\bridge_intellegence\\fel_segmentation\\" + str(i), segmented_image.astype(np.uint8))
    #key = cv2.waitKey(0) & 0xFF
    # if the `q` key was pressed, break from the loop
    #if key == ord("q"):
        #break
