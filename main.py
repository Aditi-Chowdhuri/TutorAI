import cv2
import numpy as np
from pose2vec import get_vec
import tensorflow as tf
from score import compare
import pickle
from verbal import get_percent_score

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


def compare_ref_recorded():
    sequence = []
    i = 0
    cap = cv2.VideoCapture("recorded_video.mp4")
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
        # masked = cv2.resize(mask[i], (512, 512))
        frame1 = np.uint8(cv2.cvtColor(frame1.reshape((257, 257, 3)), cv2.COLOR_BGR2RGB))
        f = cv2.resize(frame1, (512, 512))
        i += 1

    cap.release()
    model = pickle.load(open("temp.pickle", 'rb'))

    model = np.array(model)
    sequence = np.array(sequence)
    print(sequence.shape)

    mean, scores = compare(sequence, model, model.shape[0], sequence.shape[0])
    s = get_percent_score(scores[:13], 40, 90)

    return s, scores
