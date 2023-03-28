import json_stream
import json
import math
import numpy as np

camera = "vehicle5"
boats = ["vehicle0", "vehicle1", "vehicle2", "vehicle3", "vehicle4"]
dimensions = {"height": 3, "width": 4, "length": 8}
f = open('boats_in_small_fishtank/dynamics.json')
samples = json.load(f)
samples = samples["time_s"]

def get_angle_of_vector(vector):
    x = vector[0]
    y = vector[1]
    if x == 0 and y < 0:
        return math.pi * 3 / 2
    if x == 0 and y > 0:
        return math.pi / 2
    if x > 0 and y >= 0:
        return math.atan(y/x)
    if x < 0 and y > 0:
        return math.pi / 2 - math.atan(y/x)
    if x < 0 and y <= 0:
        return math.pi  + math.atan(y/x)
    if x > 0 and y < 0:
        return math.pi * 3 / 2 - math.atan(y/x)
    

def calculate_relative_yaw(camera_position, boat_position, boat_angle):
    # Translating boat angle to a vector
    a = np.array([math.cos(boat_angle), math.sin(boat_angle)])
    # Translate coordinates of boat and camera to a vector
    b = np.array([camera_position[0] - boat_position[0], camera_position[1] - boat_position[1]])

    # Calculate angle between vector a and b
    angle = math.acos(a.dot(b)/(np.linalg.norm(a) * np.linalg.norm(b)))
    
    boat_to_camera_angle = get_angle_of_vector(b)
    diff = boat_angle - boat_to_camera_angle

    if (diff > 0 and diff < math.pi) or (diff < -math.pi):
        return angle
    else:
        return -angle


def calculate_relative_position(camera_position, boat_position, angle_camera):
    #Translate camera position to origin
    x = boat_position[0] - camera_position[0]
    y = boat_position[1] - camera_position[1]

    #Rotate 
    new_x = x * math.cos(-angle_camera) - y * math.sin(-angle_camera)
    new_y = x * math.sin(-angle_camera) + y * math.cos(-angle_camera)

    return [new_x, new_y]

ground_truth_3d_bb = []
for index, step in enumerate(samples):
    sample = samples[step]
    bbs = []
    for boat in boats:
        coordinates = calculate_relative_position(sample[camera]["center_position_m"], sample[boat]["center_position_m"], sample[camera]["heading_rad"])
        angle = calculate_relative_yaw(sample[camera]["center_position_m"], sample[boat]["center_position_m"], sample[boat]["heading_rad"])
        bbs.append([coordinates[0], coordinates[1], dimensions["width"], dimensions["height"], dimensions["length"], angle])
    ground_truth_3d_bb.append(bbs)

f.close()
f2 = open("boats_in_small_fishtank/ground_truth_3d.json", "w")
json.dump(ground_truth_3d_bb, f2)
f2.close()