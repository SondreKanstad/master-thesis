import math
from utills import *
import copy
import json
from depth_estimation import get_depth

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

def associate_bb_to_bb_IoU(left, right, threshold):
    left_to_right = []
    for i in range(len(left)):
        association = -1
        IoU = 0
        for j in range(len(right)):
            tmp = calculate_IoU(left[i], right[j])
            if(tmp > threshold and tmp > IoU):
                association = j
                IoU = tmp
        left_to_right.append(association)

    for i in range(len(left)):
        association = left_to_right[i]
        if association == -1: continue
        IoU = calculate_IoU(left[i], right[association])
        if(association == -1): continue
        for j in range(i+1, len(left)):
            if(association == left_to_right[j]):
                if(IoU < calculate_IoU(left[j], right[association])):
                    left_to_right[i] = -1
                else:
                    left_to_right[j] = -1

    return left_to_right

def calculate_IoU(left, right):
    if(right[2] < left[2]):
        overlap_x = right[2] - left[0]
    else:
        overlap_x = left[2] - right[0]
    if(right[0] < left[0]):
        overlap_y = right[3] - left[1]
    else:
        overlap_y = left[3] - right[1]
    if(overlap_x < 0 or overlap_y < 0): return 0
    intersection = overlap_x * overlap_y
    areal_left = (left[2] - left[0]) * (left[3] - left[1])
    areal_right = (right[2] - right[0]) * (right[3] - right[1])
    union = areal_left + areal_right - intersection
    return intersection / union

def get_bearing_gt(ground_truth):
    if ground_truth[0] <= 0: return math.inf
    angle = math.atan(ground_truth[1] / ground_truth[0])
    if abs(angle) > 1.3: return math.inf
    return angle

def get_bearing_bb(bounding_box):
    center_bb = get_bottom_center_of_bounding_box(bounding_box)
    return math.atan((camera_center[0] - center_bb[0]) / center_bb[1])

def get_bearing_alt(bounding_box):
    center_bb = get_bottom_center_of_bounding_box(bounding_box)
    return (camera_center[0] - center_bb[0]) * field_of_view[0] / image_width

def get_center_of_bounding_box(bounding_box):
    x = (bounding_box[0] + bounding_box[2]) / 2
    y = (bounding_box[1] + bounding_box[3]) / 2
    return (x, y)

def get_bottom_center_of_bounding_box(bounding_box):
    x = (bounding_box[0] + bounding_box[2]) / 2
    y = bounding_box[1]
    return (x, y)
    
def get_squere_error(y, y_hat):
    return (y - y_hat)**2

def get_root_squere_error(y, y_hat):
    return math.sqrt(get_squere_error(y,y_hat))

f1 = open("../simulated_data/bounding_boxes_left_10cm_camera.json")
f2 = open("../simulated_data/bounding_boxes_right_10cm_camera.json")
f3 = open("../simulated_data/ground_truth_3d.json")
left_camera = json.load(f1)
right_camera = json.load(f2)
ground_truth = json.load(f3)
f1.close()
f2.close()
f3.close()

def test_depth_frame(frame):
    left_camera = left_camera[frame]
    right_camera = right_camera[frame]
    ground_truth = ground_truth[frame]

    print(left_camera)
    print(right_camera)
    print(ground_truth)
    for i in range(len(left_camera)):
        print(f"LBB {i}: {left_camera[i]}, Bearing: {get_bearing_bb(left_camera[i])}")
    for i in range(len(right_camera)):
        print(f"RBB {i}: {right_camera[i]}, Bearing: {get_bearing_bb(right_camera[i])}")
    for i in range(len(ground_truth)):
        print(f"GT {i}: {ground_truth[i]}, bearing: {get_bearing_gt(ground_truth[i])}")
    l_gt = assosiate_bounding_boxes_with_gt(left_camera, ground_truth)
    l_r = assoisiate_bb_to_bb(left_camera, right_camera)
    print(l_gt)
    print(l_r)
    for i in range(len(left_camera)):
        left_center = get_center_of_bounding_box(left_camera[i])
        right_center = get_center_of_bounding_box(right_camera[l_r[i]])
        left_left = (left_camera[i][0], left_camera[i][1])
        right_left = (right_camera[l_r[i]][0], right_camera[l_r[i]][1])
        left_right = (left_camera[i][2], left_camera[i][3])
        right_right = (right_camera[l_r[i]][2], right_camera[l_r[i]][3])
        print(f"Depth estimate center = {get_depth(left_center, right_center)}")
        print(f"Depth estimate left = {get_depth(left_left, right_left)}")
        print(f"Depth estimate right = {get_depth(left_right, right_right)}")
        print(f"Ground truth = {ground_truth[l_gt[i]][0]}")

def test_depth():
    total_error = [0,0,0,0,0]
    total_number = [0,0,0,0,0]
    number_of_good_predictions = [0,0,0,0,0]
    for frame in range(len(left_camera)):
        if(len(right_camera[frame]) != len(left_camera[frame]) or len(left_camera[frame]) > len(ground_truth[frame])): continue
        left_gt_assosiation = assosiate_bounding_boxes_with_gt(left_camera[frame], ground_truth[frame])
        left_right_assosiation = assoisiate_bb_to_bb(left_camera[frame], right_camera[frame])
        # left_right_assosiation = associate_bb_to_bb_IoU(left_camera[frame], right_camera[frame], 0.5)
        for i in range(len(left_camera[frame])):
            if(left_right_assosiation[i] == -1): continue
            left = left_camera[frame][i]
            right = right_camera[frame][left_right_assosiation[i]]
            gt = ground_truth[frame][left_gt_assosiation[i]]
            center_left = get_center_of_bounding_box(left)
            center_right = get_center_of_bounding_box(right)
            z_pred = get_depth(center_left, center_right)
            if not z_pred: continue
            if(z_pred > 100): continue
            z = gt[0]
            if z <= 0: continue
            index = math.floor(z / 20)
            if index > 4: index = 4
            error = get_root_squere_error(z, z_pred)
            if(error <= 6): number_of_good_predictions[index] += 1
            total_error[index] += error
            total_number[index] += 1

    print(f"Mean square error: {[total_error[i]/total_number[i] for i in range(len(total_error))]}")
    print(total_number)
    print(number_of_good_predictions)
    print(f"Prosentage good estimations {[number_of_good_predictions[i]/total_number[i] for i in range(len(total_error))]}")

def test_bearing():
    total_error = 0
    total_number = 0
    good_estimates = 0
    bad_estimates = 0
    for frame in range(len(left_camera)):
        if(len(right_camera[frame]) != len(left_camera[frame]) or len(left_camera[frame]) > len(ground_truth[frame])): continue
        left_gt_assosiation = assosiate_bounding_boxes_with_gt(left_camera[frame], ground_truth[frame])
        # left_right_assosiation = assoisiate_bb_to_bb(left_camera[frame], right_camera[frame])
        left_right_assosiation = associate_bb_to_bb_IoU(left_camera[frame], right_camera[frame], 0.5)
        for i in range(len(left_camera[frame])):
            if(left_right_assosiation[i] == -1): continue
            left_angle = get_bearing_alt(left_camera[frame][i])
            right_angle = get_bearing_alt(right_camera[frame][left_right_assosiation[i]])
            angle_pred = (left_angle + right_angle) / 2
            angle = get_bearing_gt(ground_truth[frame][left_gt_assosiation[i]])
            if(angle == math.inf): continue
            error = get_squere_error(angle, angle_pred)
            if(error < 0.1): good_estimates += 1
            if(error > 5): bad_estimates += 1
            total_error += error
            total_number += 1
    print(f"Mean square error: {total_error/total_number}")
    print(f"Good estimates: {good_estimates}")
    print(f"proseantage Good estimates: {good_estimates/total_number}%")
    print(f"Total estimates: {total_number}")
    print(f"Total bad estimates: {bad_estimates}")

# test_bearing()
# test_depth()