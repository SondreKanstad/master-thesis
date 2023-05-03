import math
from utills import *
import copy
import json
from depth_estimation import get_depth
from performance_testing import associate_bb_to_bb_IoU, get_bearing_alt, get_center_of_bounding_box
import matplotlib.pyplot as plt
import numpy as np



def generate_percetion():
    f1 = open("../simulated_data/bounding_boxes_left_10cm_camera.json")
    f2 = open("../simulated_data/bounding_boxes_right_10cm_camera.json")
    left_camera = json.load(f1)
    right_camera = json.load(f2)
    f1.close()
    f2.close()

    perception = []

    for frame in range(len(left_camera)):
        predictions = []
        left_right_association = associate_bb_to_bb_IoU(left_camera[frame], right_camera[frame], 0.5)
        for i in range(len(left_camera[frame])):
            if left_right_association[i] == -1: continue
            left = left_camera[frame][i]
            right = right_camera[frame][left_right_association[i]]
            left_center = get_center_of_bounding_box(left)
            rigth_center = get_center_of_bounding_box(right)
            depth = get_depth(left_center, rigth_center)
            left_bearing = get_bearing_alt(left)
            right_bearing = get_bearing_alt(right)
            bearing = (left_bearing + right_bearing) / 2
            predictions.append([depth, depth * math.tan(bearing)])
        perception.append(predictions)
    f = open("predictions.json", "w")
    json.dump(perception, f)
    f.close()

# generate_percetion()

# frame = 2400

# f1 = open("predictions.json")
# f3 = open("../simulated_data/ground_truth_3d.json")
# predictions = json.load(f1)
# ground_truth = json.load(f3)
# f1.close()
# f3.close()

# print(f"Predictions: {predictions[2400]}")
# print(f"Ground truth: {ground_truth[2400]}")

def get_distance(pred, gt):
    return math.sqrt((pred[0] - gt[0])**2 + (pred[1] - gt[1])**2)

def get_bearing_gt(ground_truth):
    angle = math.atan(ground_truth[1] / ground_truth[0])
    return angle

def calculate_root_square_error():
    f1 = open("predictions.json")
    f2 = open("../simulated_data/ground_truth_3d.json")
    predictions = json.load(f1)
    ground_truth = json.load(f2)
    f1.close()
    f2.close()

    total_distance = 0
    total_predictions = 0
    good_estiamtes_count = 0
    bad_estimates_count = 0
    distances = []
    bearings = [0,0,0,0]
    number_of_bearings = [0,0,0,0]
    distances_target = [0,0,0,0,0]
    number_of_distances_target = [0,0,0,0,0]


    for frame in range(len(predictions)):
        for pred in predictions[frame]:
            distance = math.inf
            bearing = 0
            index_dist = 0
            for gt in ground_truth[frame]:
                d = get_distance(pred, gt)
                if d < distance: 
                    distance = d
                    bearing = min(abs(int(get_bearing_gt(gt) / 0.738)), 3)
                    index_dist = min(int(math.sqrt(gt[0]**2 + gt[1]**2) / 20), 4)
            if distance < 2: 
                good_estiamtes_count += 1
                bearings[bearing] += 1
                distances_target[index_dist] += 1
            if distance > 40: bad_estimates_count += 1
            distances.append(distance)
            total_distance += distance
            total_predictions += 1
            number_of_bearings[bearing] += 1
            number_of_distances_target[index_dist] += 1
    print(f"{good_estiamtes_count} good estimates out of {total_predictions}")
    print(f"{bad_estimates_count} bad estimates out of {total_predictions}")
    print(f"Avarege distance: {total_distance/total_predictions}")
    for i in range(len(bearings)):
        print(f"Average distance sone {i+1}: {bearings[i]/number_of_bearings[i] if number_of_bearings[i] > 0 else 0}")
    for i in range(len(distances_target)):
        print(f"Average distance {i * 20} to {(i+1) * 20}: {distances_target[i]/number_of_distances_target[i] if number_of_distances_target[i] > 0 else 0}")
    
    # a = np.array(distances)
    # fig, ax = plt.subplots(figsize =(10, 7))
    # _, bins, patches = plt.hist(a, bins=[0,5,10,15,20,25,30, 35, 40, 45], edgecolor="black")#, rwidth=0.7)
    # xlabels = bins[0:].astype(str)
    # for i in range(len(xlabels)-1):
    #     xlabels[i] += "m"
    # xlabels[-2] += '+'
    # xlabels[-1] = ""
    # plt.xlim([0, 45])
    # plt.xlabel("Distance from Ground Truth", fontsize=16)
    # plt.ylabel("Number of occurrences", fontsize=16)
    # ax.set_title("Position Prediction Error Histogram", fontsize=22)
    # ax.set_xticklabels(xlabels)
    # plt.savefig("position_error_hist")

calculate_root_square_error()
# generate_percetion()
