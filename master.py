from skimage.io import imread
import os
import matplotlib.pyplot as plt
from picoyplaca import picoyplaca_program
from picoyplaca import license_plate_detection

"""
Part 1 - Detect the license plate ID directly from the picture of the car
"""

# Load the picture:
current_dir = os.path.dirname(os.path.realpath(__file__))
image_path = os.path.join(current_dir, 'picoyplaca/car_image/car.jpg')
car_image = imread(image_path)
# plot the picture
fig, ax1 = plt.subplots(1)
ax1.imshow(car_image)
plt.show()
# change to gray colors
car_image = imread(image_path, as_gray=True)

# Detect and get as string the license plate ID from the picture
plate_ID_detection = license_plate_detection.class_license_plate_ID_detection
plate_ID_detection.license_plate_ID_detection(car_image)

"""
Part 2 - Test whether the car can be on the road
"""

# We can use the license plate ID that was detected from the image or
# we can just enter any other license plate ID

# 2) Run pico y placa program
picoyplaca = picoyplaca_program.classPicoyPlaca
picoyplaca.pico_y_placa()




