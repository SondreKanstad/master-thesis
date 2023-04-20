import math
from utills import *
import copy
import json
from depth_estimation import get_center_of_bounding, get_depth

def assosiate_bounding_boxes_with_gt(bounding_boxes, ground_truths):
    bb_bearings = []
    bb_to_gt = []
    for bb in bounding_boxes:
        bb_bearings.append(get_bearing_bb(bb))
    gt_bearings = []
    gt_indecies = [i for i in range(len(ground_truths))]
    for gt in ground_truths:
        gt_bearings.append(get_bearing_gt(gt))
    while(len(bb_bearings) < len(gt_bearings)):
        index = -1
        value = 0
        for i in range(len(gt_bearings)):
            if abs(gt_bearings[i] > value):
                value = abs(gt_bearings[i])
                index = i
        gt_bearings.pop(index)
        gt_indecies.pop(index)
    sorted_bb_bearings = copy.deepcopy(bb_bearings)
    sorted_gt_bearings = copy.deepcopy(gt_bearings)
    sorted_bb_bearings.sort()
    sorted_gt_bearings.sort()
    for i in range(len(bb_bearings)):
        bb_index = sorted_bb_bearings.index(bb_bearings[i])
        gt_index = gt_bearings.index(sorted_gt_bearings[bb_index])
        bb_to_gt.append(gt_indecies[gt_index])
    return bb_to_gt

def assoisiate_bb_to_bb(left, right):
    left_bearings = []
    left_to_right = []
    for bb in left:
        left_bearings.append(get_bearing_bb(bb))
    right_bearings = []
    for bb in right:
        right_bearings.append(get_bearing_bb(bb))
    sorted_left_bearings = copy.deepcopy(left_bearings)
    sorted_right_bearings = copy.deepcopy(right_bearings)
    sorted_left_bearings.sort()
    sorted_right_bearings.sort()
    for i in range(len(left_bearings)):
        left_index = sorted_left_bearings.index(left_bearings[i])
        right_index = right_bearings.index(sorted_right_bearings[left_index])
        left_to_right.append(right_index)
    return left_to_right


def get_bearing_gt(ground_truth):
    if ground_truth[0] <= 0: return math.inf 
    return math.atan(ground_truth[1] / ground_truth[0])

def get_bearing_bb(bounding_box):
    center_bb = get_center_of_bounding_box(bounding_box)
    return math.atan((camera_center[0] - center_bb[0]) / center_bb[1])

def get_center_of_bounding_box(bounding_box):
    x = (bounding_box[0] + bounding_box[2]) / 2
    y = (bounding_box[1] + bounding_box[3]) / 2
    return (x, y)
    
def get_squere_error(y, y_hat):
    return (y - y_hat)**2

f1 = open("../simulated_data/bounding_boxes_left_10cm_camera.json")
f2 = open("../simulated_data/bounding_boxes_right_10cm_camera.json")
f3 = open("../simulated_data/ground_truth_3d.json")
left_camera = json.load(f1)
right_camera = json.load(f2)
ground_truth = json.load(f3)
f1.close()
f2.close()
f3.close()


# frame = 2900
# left_camera = left_camera[frame]
# right_camera = right_camera[frame]
# ground_truth = ground_truth[frame]

# print(left_camera)
# print(right_camera)
# print(ground_truth)
# for i in range(len(left_camera)):
#     print(f"LBB {i}: {left_camera[i]}, Bearing: {get_bearing_bb(left_camera[i])}")
# for i in range(len(right_camera)):
#     print(f"RBB {i}: {right_camera[i]}, Bearing: {get_bearing_bb(right_camera[i])}")
# for i in range(len(ground_truth)):
#     print(f"GT {i}: {ground_truth[i]}, bearing: {get_bearing_gt(ground_truth[i])}")
# l_gt = assosiate_bounding_boxes_with_gt(left_camera, ground_truth)
# l_r = assoisiate_bb_to_bb(left_camera, right_camera)
# print(l_gt)
# print(l_r)
# for i in range(len(left_camera)):
#     left = get_center_of_bounding_box(left_camera[i])
#     right = get_center_of_bounding_box(right_camera[l_r[i]])
#     print(f"Depth estimate = {get_depth(left, right)}")
#     print(f"Ground truth = {ground_truth[l_gt[i]][0]}")

total_error = [0,0,0,0,0]
total_number = [0,0,0,0,0]
areas = []
number_of_good_predictions = [0,0,0,0,0]
for frame in range(len(left_camera)):
    if(len(right_camera[frame]) != len(left_camera[frame]) or len(left_camera[frame]) > len(ground_truth[frame])): continue
    left_gt_assosiation = assosiate_bounding_boxes_with_gt(left_camera[frame], ground_truth[frame])
    left_right_assosiation = assoisiate_bb_to_bb(left_camera[frame], right_camera[frame])
    for i in range(len(left_camera[frame])):
        left = left_camera[frame][i]
        right = right_camera[frame][left_right_assosiation[i]]
        gt = ground_truth[frame][left_gt_assosiation[i]]
        center_left = get_center_of_bounding(left)
        center_right = get_center_of_bounding(right)
        z_pred = get_depth(center_left, center_right)
        if not z_pred: continue
        if(z_pred > 100): continue
        z = gt[0]
        if z <= 0: continue
        index = math.floor(z / 10)
        if index > 4: index = 4
        error = get_squere_error(z, z_pred)
        if(error < 1): number_of_good_predictions[index] += 1
        total_error[index] += error
        total_number[index] += 1

print(f"Mean square error: {[total_error[i]/total_number[i] for i in range(len(total_error))]}")
print(total_number)
print(number_of_good_predictions)