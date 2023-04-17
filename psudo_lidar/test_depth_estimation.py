import json
import math
from depth_estimation import *

frame = 2400

f1 = open("../simulated_data/bounding_boxes_left_camera.json")
f2 = open("../simulated_data/bounding_boxes_right_camera.json")
f3 = open("../simulated_data/ground_truth_3d.json")
left_camera = json.load(f1)
right_camera = json.load(f2)
ground_truth = json.load(f3)
f1.close()
f2.close()
f3.close()

left_camera = left_camera[frame]
right_camera = right_camera[frame]
ground_truth = ground_truth[frame]


bounding_boxes_left = []
bounding_boxes_right = []
for i in range(len(left_camera)):
    bounding_boxes_left.append([])
    bounding_boxes_right.append([])
    for j in range(len(left_camera[i])):
        x = 0 if j < 2 else 2
        y = j % 2 * 2 + 1
        bounding_boxes_left[i].append((left_camera[i][x], left_camera[i][y]))
        bounding_boxes_right[i].append((right_camera[i][x], right_camera[i][y]))

print(bounding_boxes_left)
print(bounding_boxes_right)
print("Depth estimations:")
for i in range(len(bounding_boxes_left)):
    print(f"Box {i + 1}: bottom left: {get_depth(bounding_boxes_left[i][0], bounding_boxes_right[i][0])}, bottom right: {get_depth(bounding_boxes_left[i][1], bounding_boxes_right[i][1])}, top left: {get_depth(bounding_boxes_left[i][2], bounding_boxes_right[i][2])}, top right: {get_depth(bounding_boxes_left[i][3], bounding_boxes_right[i][3])}")
print("Ground truths:")
for element in ground_truth:
    if element[0] > 0 and element[1] < 50 and element[1] > -50:
        print(f"{element[0]}")