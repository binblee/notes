import cv2
import numpy as np
import os
import sys

def read_images(path, image_size):
    names = []
    training_images, training_labels = [], []
    label = 0
    for dirname, dirnames, filenames in os.walk(path):
        for subdirname in dirnames:
            names.append(subdirname)
            subject_path = os.path.join(dirname, subdirname)
            for filename in os.listdir(subject_path):
                img = cv2.imread(os.path.join(subject_path, filename), cv2.IMREAD_GRAYSCALE)
                if (img is None):
                    continue
                # resize to given size (if given)
                img = cv2.resize(img, image_size)
                training_images.append(img)
                training_labels.append(label)
            label += 1
    training_images = np.asarray(training_images, np.uint8)
    training_labels = np.asarray(training_labels, np.int32)
    return names, training_images, training_labels
            

