# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 10:17:43 2020

@author: chinjooern
"""
import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split


EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4



def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
                                                                                                        
    subdirs = [x[0] for x in os.walk(data_dir)]  
    print(subdirs)
    main_dir = subdirs[0]
    subdirs = subdirs[1:]
    print(subdirs)                                                                         
    images = []
    labels = []
    
    dim = (IMG_WIDTH,IMG_HEIGHT)

    for folder in subdirs:
        print(folder)
        filenames = os.walk(folder).__next__()[2]
        for filename in filenames:
            img = cv2.imread(os.path.join(folder,filename))
            if img is not None:
                resized_img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
                images.append(resized_img)
                labels.append(folder.split(main_dir)[-1][1:])
                
    return((images,labels))



test_images, test_labels = load_data(r'C:\Users\chinjooern\Desktop\traffic\traffic\gtsrb')
# Sample test data
test_labels = tf.keras.utils.to_categorical(test_labels)
x_train, x_test, y_train, y_test = train_test_split(
    np.array(test_images), np.array(test_labels), test_size=TEST_SIZE
)
# Recreate the exact same model, including its weights and the optimizer
new_model = tf.keras.models.load_model('model.h5')

# Show the model architecture
new_model.summary()


loss, acc = new_model.evaluate(test_images,  test_labels, verbose=2)
print('Restored model, accuracy: {:5.2f}%'.format(100*acc))