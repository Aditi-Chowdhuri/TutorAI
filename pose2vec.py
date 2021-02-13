def get_vec(pose):
    vec = []
    vec.append(pose[5]-pose[6])
    vec.append(pose[5]-pose[7])
    vec.append(pose[6]-pose[8])
    vec.append(pose[7]-pose[9])
    vec.append(pose[8]-pose[10])
    vec.append(pose[5]-pose[11])
    vec.append(pose[6]-pose[12])
    vec.append(pose[11]-pose[12])
    vec.append(pose[11]-pose[13])
    vec.append(pose[12]-pose[14])
    vec.append(pose[13]-pose[15])
    vec.append(pose[14]-pose[16])

    x = (pose[5][0]+pose[6][0])/2
    y = (pose[5][1]+pose[6][1])/2

    vec.append([x, y] - pose[0])

    return vec

info = ['left-right shoulder', 'left shoulder-elbow', 'right shoulder-elbow', 'left elbow-wrist', 'right elbow-wrist', 'left shoulder-hip', 'right shoulder-hip', 'left-right hip', 'left hip-knee', 'right hip-knee', 'left knee-ankle', 'right knee-ankle', 'shoulders mid-nose']