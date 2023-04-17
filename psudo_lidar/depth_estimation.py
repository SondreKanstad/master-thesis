from utills import *

def get_disprity(pixel_left, pixel_right):
    return (pixel_left[0] - pixel_right[0], pixel_left[1] - pixel_right[1])


def get_width(pixel_left, depth):
    return (pixel_left[0] - camera_center[0]) * depth / horizontal_focal_length

def get_height(pixel_left, depth):
    return (pixel_left[1] - camera_center[1]) * depth / vertical_focal_length

def get_depth(pixel_left, pixel_right):
    disparity = get_disprity(pixel_left, pixel_right)[0]
    if disparity <= 0: disparity = 0.1
    return horizontal_focal_length * baseline / disparity

def pixel_to_3d_coordinate(pixel_left, pixel_right):
    z = get_depth(pixel_left, pixel_right)
    x = get_width(pixel_left, z)
    y = get_height(pixel_left, z)
    return (x, y, z)

def get_center_of_bounding(top_left, bottom_left, top_right):
    x = (top_left[0] + top_right[0]) / 2
    y = (top_left[1] + bottom_left[1]) / 2
    return (x, y)
