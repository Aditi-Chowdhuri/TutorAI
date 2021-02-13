import pickle
import numpy as np
import math



dictionary = dict({0: 'shoulders', 1: 'left hand', 2: 'right hand', 3: 'left forearm', 4: 'right forearm', 5: 'left side of the body',
                   6: 'right side of the body', 7: 'waist', 8: 'left thigh', 9: 'right thigh', 10: 'left crus', 11: 'right crus', 12: 'Head'})

arr = [99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99]

# takes in array of keypoints of all frames contained in pickle file
def imp_parts_to_focus_on(target_arr):
    target_arr = np.asarray(target_arr)
    diff = np.zeros([12, 2])

    for i in range(0, target_arr.shape[0]-1):   # find changes in each body part
        for j in range(target_arr.shape[1]):
            x1, y1 = target_arr[i][j]
            x2, y2 = target_arr[i+1][j]
            sub = math.sqrt((x1-x2) ^ 2 + (y1-y2) ^ 2)
            diff[j][1] = j
            diff[j][0] += sub

    diff = diff[np.argsort(diff[:, 0])]
    ref = [0, 1, 2, 5, 8, 9]
    change = []
    c = 0
    for i in diff: # find the top changes and tell the user to focus on on that area
        if c > 2:
            break
        else:
            if i[1] in ref:
                change.append(i[1])
                c += 1

    s = "For this tutorial try to focus more on"
    if 1 in change or 2 in change:
        s += " hands,"
    if 8 in change or 9 in change:
        s += " legs,"
    if 0 in change or 5 in change:
        s += " Upper body,"



# takes the excercise pickle file as the input and displays the instructions for that excercise
def initial_instructions(pick_file):
    s = "General Instructions before starting:-\n"
    b = pickle.load(open(pick_file, 'rb'))
    for (k, v) in b.items():
        if k == 'instructions':
            s += v



# function to display the different errors user makes while doing the excercise
# To be called after every video loop until the user does it perfectly
# takes in the percent score array given by dtw and lower and upper threshold for checking
def get_percent_score(score, lt, ht):
    s = ""
    c = 0
    for i in score:
        if i > ht:
            c = c + 1

    if c == 13:
        s = "Congratulations! you have mastered this Pose.\n"


    else:
        #[0, 1, 2, 7, 8, 9, 12], # Main Body Parts
        keys = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                [0, 5, 6, 7], # Upper Body
                [1, 3],  # Left Hand
                [2, 4],  # Right Hand
                [8, 10], # Left Leg
                [9, 11], # Right Leg
                [12]]    # Head

        # Major Errors
        temp = []
        for i in range(len(score)):
            if score[i] <= lt:
                temp.append(dictionary.get(i))

        if len(temp) != 0:
            s += "Major Errors are:-\n"
            for part in temp:
                s += part + ".\n"
            s += "\n"
        else:
            s += "You are doing good, there are no major errors as such but keep trying until you get the perfect posture\n\n"

        # Torso
        if (lt <= score[keys[1][0]] <= ht) and (lt <= score[keys[1][1]] <= ht) and (lt <= score[keys[1][2]] <= ht) and (lt <= score[keys[1][3]] <= ht):
            s += "You are almost getting your Torso correct, keep working on it.\n"

        if (score[keys[1][0]] > ht) and (score[keys[1][1]] > ht) and (score[keys[1][2]] > ht) and (score[keys[1][3]] > ht):
            s += "Amazing, You got your Upper Body Posture correct.\n"


        # Hands
        if (lt <= score[keys[2][0]] <= ht) and (lt <= score[keys[3][0]] <= ht):
            s += "Your Hands were almost correct, but not perfect.\n"

        if score[keys[2][0]] > ht and (lt <= score[keys[2][1]] <= ht):
            s += "Your Left Forearms do not match.\n"

        if score[keys[3][0]] > ht and (lt <= score[keys[3][1]] <= ht):
            s += "Your Right Forearms do not match.\n"

        if score[keys[2][0]] > ht and score[keys[2][1]] > ht and score[keys[3][0]] > ht and score[keys[3][1]] > ht:
            s += "Great! Your hands are perfect.\n"


        # Legs
        if (lt <= score[keys[4][0]] <= ht) and (lt <= score[keys[5][0]] <= ht):
            s += "Your legs were almost correct, but not perfect.\n"

        if score[keys[4][0]] > ht and (lt <= score[keys[4][1]] <= ht):
            s += "Left Crus do not match.\n"

        if score[keys[5][0]] > ht and (lt <= score[keys[5][1]] <= ht):
            s += "Right Crus do not match.\n"

        if score[keys[4][0]] > ht and score[keys[4][1]] > ht and score[keys[5][0]] > ht and score[keys[5][1]] > ht:
            s += "Nice Work!, Your legs are perfect.\n"

        # Head
        if lt <= score[keys[6][0]] <= ht:
            s += "Your Head posture is not perfect.\n"

        if score[keys[6][0]] > ht:
            s += "Great! Your Head posture is correct.\n"


        if len(temp) != 0:
            s += "\nNote: You should try focusing on correcting the major errors first and then the other ones\n"
        else:
            s += "\nNote: You are almost there, a little more effort and you will master this pose\n"



    return s

# imp_parts_to_focus_on(arr)

