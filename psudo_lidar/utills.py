import math

camera_center = (1920/2, 1080/2)
vertical_focal_length = 25 #Given in millimeters
horizontal_focal_length = 25 #Given in millimeters
baseline = 35
image_width = 1920
image_height = 1080 
# field_of_view = (127 / 180) * math.pi
# angle_per_pixel = field_of_view / math.sqrt(image_height**2 + image_width**2)


focal_length = [horizontal_focal_length, vertical_focal_length]
principal_point = camera_center
field_of_view = [2 * math.atan(image_width / (2 * focal_length[0])), 2 * math.atan(image_height / (2 * focal_length[1]))]