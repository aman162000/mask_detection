import numpy
import cv2
import face_recognition as fr
import time
import encodes
import message
import requests
from firebase import firebase
from imutils.video import VideoStream


webcam = VideoStream(src=0).start()
prevTime = 0
# path = "Images"
# image_list = os.listdir(path)
# print(image_list)
# image_names = []
# image = []
# for img in image_list:
#     current_image = cv2.imread(f'{path}/{img}')
#     image.append(current_image)
#     image_names.append(os.path.splitext(img)[0])


# def encoding_of_images(image):
#     list_of_encoding = []
#     for i in image:
#         i = cv2.cvtColor(i, cv2.COLOR_BGR2RGB)
#         encode = fr.face_encodings(i)[0]
#         list_of_encoding.append(encode)
#     print("Encoding Done")
#     return list_of_encoding


# enc = encoding_of_images(image)

class Break(Exception): pass

print('Starting...')
try:
    while True:
        raw_img = webcam.read()
        webcam_img = cv2.flip(raw_img, 3)
        image_small = cv2.resize(webcam_img, (0, 0), None, 0.25, 0.25)
        image_small = cv2.cvtColor(image_small, cv2.COLOR_BGR2RGB)
        face_location = fr.face_locations(image_small)
        encode_current_face = fr.face_encodings(image_small, face_location)

        curTime = time.time()
        sec = curTime - prevTime
        prevTime = curTime

        fps = 1 / (sec)

        str = "FPS : %0.1f" % fps
        cv2.putText(webcam_img, str, (0, 110), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))

        for encode_current, face_current in zip(encode_current_face, face_location):
            face_match = fr.compare_faces(encode_current, encodes.en)
            dist = fr.face_distance(encode_current, encodes.en)
            index_match = numpy.argmin(dist)

            if face_match[index_match]:
                name = encodes.names[index_match]
                # message.msg(name)
                # time.sleep(10*5)
                cv2.rectangle(webcam_img, (face_current[3] * 4, face_current[0] * 4),
                              (face_current[1] * 4, face_current[2] * 4), (00, 00, 255), 5)
                cv2.putText(webcam_img, name, (face_current[3] * 4, face_current[2] * 4 + 20), cv2.FONT_HERSHEY_COMPLEX,
                            1, (255, 255, 255,), 2)

            else:

                cv2.rectangle(webcam_img, (face_current[3] * 4, face_current[0] * 4), (face_current[1] * 4, face_current[2] * 4), (00, 00, 255), 5)
                cv2.putText(webcam_img, "Invalid Person", (face_current[3] * 4, face_current[2] * 4 + 20), cv2.FONT_HERSHEY_COMPLEX,1, (255, 255, 255,), 2)
                # if cv2.waitKey(0) == 27:
                #raise Break

        cv2.imshow("Webcam", webcam_img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except Break:
    print("Invalid Person")