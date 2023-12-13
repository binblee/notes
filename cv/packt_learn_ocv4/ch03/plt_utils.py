import cv2
import matplotlib.pyplot as plt

def plt_imgshow(img, cvtColor=cv2.COLOR_BGR2RGB):
    img_rgb = cv2.cvtColor(img, cvtColor)
    plt.imshow(img_rgb)