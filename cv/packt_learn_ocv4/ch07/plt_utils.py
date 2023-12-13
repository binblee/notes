import cv2
import matplotlib.pyplot as plt
import math

def plt_imgshow(imgs, cvtColor=cv2.COLOR_BGR2RGB, columns=1):
    if type(imgs) == list:
        row = math.ceil(len(imgs) / columns)
        for idx, img in enumerate(imgs):
            plt.subplot(row,columns,idx+1)
            plt.imshow(cv2.cvtColor(img, cvtColor))
    else:
        plt.imshow(cv2.cvtColor(imgs, cvtColor))
