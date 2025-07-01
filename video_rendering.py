import math
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from shapely.affinity import rotate, translate
from shapely.ops import unary_union


import os

import cv2
import os
from natsort import natsorted

output_dir = "configs_by_phi"  
os.makedirs(output_dir, exist_ok=True)

image_folder = 'rendered_video'  # Folder containing .png images
output_dir = 'rendered_video'
output_filename = 'phi_demo.mp4'
fps = 1  # Frames per second

os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, output_filename)

images = natsorted([f for f in os.listdir(image_folder) if f.endswith('.png')])
# Read the first image to get video dimensions
first_img = cv2.imread(os.path.join(image_folder, images[0]))
height, width, _ = first_img.shape

# Set up the video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

# Write each image frame to the video
for img_name in images:
    img_path = os.path.join(image_folder, img_name)
    frame = cv2.imread(img_path)
    video.write(frame)

video.release()
print(f"Video saved to: {output_path}")

