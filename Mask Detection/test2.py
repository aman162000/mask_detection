import csv
import pandas as pd
import numpy as np
import os
import cv2
import face_recognition as fr
images = []
image_names = []
path = "Images"
for img in os.listdir(path):
    current_image = cv2.imread(f'{path}/{img}')
    images.append(current_image)
    image_names.append(os.path.splitext(img)[0])

list_of_encoding = []
def encoding_of_images(image):
    for i in image:
        i = cv2.cvtColor(i , cv2.COLOR_BGR2RGB)
        encode = fr.face_encodings(i)[0]
        list_of_encoding.append(encode)
    print("Encoding Done")

    return list_of_encoding

print(encoding_of_images(images))
