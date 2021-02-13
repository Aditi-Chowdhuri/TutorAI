import numpy as np
from dtaidistance import dtw

def percentage_score(score):
    percentage = 100 - (score * 100)
    return int(percentage)

def dtwdis(input_points, model_points, i, j):
    input_pts = input_points.reshape(2 * j,)
    model_pts = model_points.reshape(2 * i,)
    model_pts = model_pts / np.linalg.norm(model_pts)
    input_pts = input_pts / np.linalg.norm(input_pts)

    return percentage_score(dtw.distance(model_pts, input_pts))

def normalize(input_test):
    for k in range(0, 13):
        input_test[:, k] = input_test[:, k] / np.linalg.norm(input_test[:, k])
    return input_test

def compare(ip, model, i, j):
    ip = normalize(ip)
    scores = []
    for k in range(0, 13):
        scores.append(dtwdis(ip[:, k], model[:, k], i, j))
    return np.mean(scores), scores
