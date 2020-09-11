# import csv oyissuqJi3O2GmYS
# import pandas as pd
# import numpy
# import os
# import cv2
# import face_recognition as fr
# images = []
# image_names = []
# path = "Images"
# for img in os.listdir(path):
#     current_image = cv2.imread(f'{path}/{img}')
#     images.append(current_image)
#     image_names.append(os.path.splitext(img)[0])
#
# list_of_encoding = []
# def encoding_of_images(image):
#
#     for i in image:
#         i = cv2.cvtColor(i , cv2.COLOR_BGR2RGB)
#         encode = fr.face_encodings(i)[0]
#         list_of_encoding.append(encode)
#     print("Encoding Done")
#     return list_of_encoding
#
# # print(encoding_of_images(images))
# import message
# for i in range(0,4):
#     message.msg('Aman')
#
# import firebase_admin
# from firebase_admin import credentials,db
#
# #credentials for connection to firebase database
# cred = credentials.Certificate('E:\Aman\Python Project\Fine Collection\payment\secretkey.json')
# firebase_admin.initialize_app(cred, {'databaseURL': 'https://mask-detection-e7ec2.firebaseio.com/'})
# # payment = db.reference('Tables/Payment')
# val =[]
# no = 9724504201
# pend = db.reference('Tables/Pending/Names/yl52cf').get()
# print(pend)
# # for i, j in payment.get().items():
# #     temp = i
# #     if type(j) is dict:
# #         for a, b in j.items():
# #             if a == "Nilesh":
# #                 print(temp)
# #             else:
# #                 temp=None

from tensorflow.keras.models import load_model
from imutils.video import VideoStream
import numpy as np
import cv2
import message
import os
import encodes
import face_recognition as fr

model = load_model('model-011.model')

face_clsfr=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

source=cv2.VideoCapture(0)

labels_dict={0:'MASK',1:'NO MASK'}
color_dict={0:(0,255,0),1:(0,0,255)}

while (True):

    ret, img = source.read()
    webcam_img = cv2.flip(img, 3)
    gray = cv2.cvtColor(webcam_img, cv2.COLOR_BGR2GRAY)
    faces = face_clsfr.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        face_img = gray[y:y + w, x:x + w]
        resized = cv2.resize(face_img, (100, 100))
        normalized = resized / 255.0
        reshaped = np.reshape(normalized, (1, 100, 100, 1))
        result = model.predict(reshaped)
        print(result)
        label = np.argmax(result, axis=1)[0]
        print(label)

        if label == 1:
            image_small = cv2.resize(webcam_img, (0, 0), None, 0.25, 0.25)
            image_small = cv2.cvtColor(image_small, cv2.COLOR_BGR2RGB)
            face_location = fr.face_locations(image_small)
            encode_current_face = fr.face_encodings(image_small, face_location, model='cnn')
            for encode_current, face_current in zip(encode_current_face, face_location):
                face_match = fr.compare_faces(encode_current, encodes.en, tolerance=0.599)
                dist = fr.face_distance(encode_current, encodes.en)
                index_match = np.argmin(dist)

                if face_match[index_match]:
                    name = encodes.names[index_match]
                    # message.msg(name)
                    cv2.rectangle(webcam_img, (face_current[3] * 4, face_current[0] * 4),
                                  (face_current[1] * 4, face_current[2] * 4), (00, 00, 255), 5)
                    cv2.putText(webcam_img, name, (face_current[3] * 4, face_current[2] * 4 - 150), cv2.FONT_HERSHEY_SIMPLEX,
                                1, (0, 255, 0,), 2)

                else:

                    cv2.rectangle(webcam_img, (face_current[3] * 4, face_current[0] * 4),
                                  (face_current[1] * 4, face_current[2] * 4), (00, 00, 255), 5)
                    cv2.putText(webcam_img, "Invalid Person", (face_current[3] * 4, face_current[2] * 4 + 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255,), 2)

        else:
            cv2.putText(webcam_img, labels_dict[label], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            cv2.rectangle(webcam_img, (x, y), (x + w, y + h), color_dict[label], 2)
            cv2.rectangle(webcam_img, (x, y - 40), (x + w, y), color_dict[label], -1)
            cv2.putText(webcam_img, labels_dict[label], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.imshow('Mask Detection', webcam_img)
    key = cv2.waitKey(1)

    if (key == 27):
        break

cv2.destroyAllWindows()
source.release()