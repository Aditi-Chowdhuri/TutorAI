# Generates the Pickle File of the Reference Video


import tensorflow as tf
import matplotlib.pyplot as plt
import math
import cv2
import numpy as np
import argparse
import pickle
from pose2vec import get_vec


# ap = argparse.ArgumentParser()
#
# ap.add_argument("-a", "--activity", required=True,
# help="activity to be recorder")
# ap.add_argument("-v", "--video", required=True,
# 	help="video file from which keypoints are to be extracted")
# args = vars(ap.parse_args())

def imgprep(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    a = np.uint8(np.zeros((img.shape[1], img.shape[1], 3)))
    a[:img.shape[0], :, :] = img[:, :, :]
    img = cv2.resize(a, (257, 257))
    img = np.copy(img)
    img = np.reshape(img, (1, 257, 257, 3))
    img = np.float32(img)
    return (img - 127.5) / 127.5

def poseproc(img):
    a = interpreter.set_tensor(input_details[0]['index'], img)
    interpreter.invoke()
    hm = interpreter.get_tensor(output_details[0]['index'])
    ofs = interpreter.get_tensor(output_details[1]['index'])
    hm = 1 / (1 + np.exp(-hm))
    hm = np.reshape(hm, (9, 9, 17))
    ofs = np.reshape(ofs, (9, 9, 34))
    kp = list()
    poq = list()
    for i in range(17):
        q, w = np.unravel_index(hm[:, :, i].argmax(), hm[:, :, i].shape)
        poq.append(hm[q, w, i])
        e = ofs[q, w, i]
        r = ofs[q, w, i+17]
        kp.append([r + ((w / 8.0) * 256), e + ((q / 8.0) * 256)])
    kp = np.array(kp)
    kp = np.uint32(np.round(kp))

    return kp, poq

interpreter = tf.lite.Interpreter(model_path="posenet.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

sequence = [] 

def get_video():
    cap = cv2.VideoCapture("ref_video.mp4")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame1 = imgprep(frame)
        dots, jk = poseproc(frame1)
        dots = dots.astype(np.int16)
        dots = get_vec(dots)
        sequence.append(dots)
        frame1 = frame1 * 127.5 + 127.5
        thresh = 0.03
        frame1 = np.uint8(cv2.cvtColor(frame1.reshape((257, 257, 3)), cv2.COLOR_BGR2RGB))
        for i in range(17):
            try:
                if jk[i] > thresh:
                    cv2.circle(frame1, (dots[i, 0], dots[i, 1]), 5, (255, 255, 255), -1)
            except:
                pass

    cap.release()

    path = "temp.pickle"
    f = open(path, 'wb')
    pickle.dump(sequence, f)
