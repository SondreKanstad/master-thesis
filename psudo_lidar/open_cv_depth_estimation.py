import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import json

def bounding_box_to_image(bounding_boxes, dimensions_x, dimensions_y):
    img = np.zeros((dimensions_y, dimensions_x), dtype = np.uint8)
    for bb in bounding_boxes:
        img[int(bb[1]) : int(bb[3]), int(bb[0]) : int(bb[2])] = np.ones((int(bb[3] - bb[1]), int(bb[2] - bb[0])), dtype = np.uint8)*255
    return img

# frame = 2400
# f1 = open("../simulated_data/bounding_boxes_left_camera.json")
# f2 = open("../simulated_data/bounding_boxes_right_camera.json")
# #f3 = open("../simulated_data/ground_truth_3d.json")
# left_camera = json.load(f1)
# right_camera = json.load(f2)
# #ground_truth = json.load(f3)
# f1.close()
# f2.close()
# #f3.close()
# left_camera = left_camera[frame]
# right_camera = right_camera[frame]

# img_left = bounding_box_to_image(left_camera, 1920, 1080)
# img_right = bounding_box_to_image(right_camera, 1920, 1080)

# plt.imshow(img_left, "gray")
# plt.show()
# plt.imshow(img_right, "gray")
# plt.show()


# img_left = cv.imread('img_left.png', cv.IMREAD_GRAYSCALE)
# img_right = cv.imread('img_right.png', cv.IMREAD_GRAYSCALE)
img_left = cv.imread('left_img.png')
img_right = cv.imread('right_img.png')

g_img_left = cv.cvtColor(img_left, cv.COLOR_BGR2GRAY)
g_img_right = cv.cvtColor(img_right, cv.COLOR_BGR2GRAY)

stereo = cv.StereoBM_create(numDisparities=0, blockSize=21)
disparity = stereo.compute(g_img_left, g_img_right)

plt.imshow(disparity, "gray")
plt.show()

# from PIL import Image
# im = Image.fromarray(img_left, mode="L")
# im.save("img_left.png")
# im = Image.fromarray(img_right, mode="L")
# im.save("img_right.png")
