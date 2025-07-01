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

image_folder = 'configs_by_phi'
output_dir = 'rendered_video'
output_filename = 'phi_demo.mp4'
fps = 1  # Frames per second

os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, output_filename)

#function to define a pacman shape
def create_pacman(radius=1, mouth_angle_deg=30, segments=100):
    theta = math.radians(mouth_angle_deg / 2)
    arc = [(radius * math.cos(a), radius * math.sin(a))
           for a in np.linspace(theta, 2 * math.pi - theta, segments)]
    return Polygon([(0, 0)] + arc + [(0, 0)])

#function to create circle (use to cut a C shape)
def create_circle(radius=0.75, segments=100):
    arc = [(radius * math.cos(a), radius * math.sin(a))
           for a in np.linspace(0, 2 * math.pi, segments)]
    return Polygon([(0, 0)] + arc + [(0, 0)])

#function to define the "boundary"
def create_outer_radii(radius=2.5, segments=100):
    arc = [(radius * math.cos(a), radius * math.sin(a))
           for a in np.linspace(0, 2 * math.pi, segments)]
    return Polygon([(0, 0)] + arc + [(0, 0)])

#function to plot the shapes with zip (solving the issue of plotting polygons with holes))
def plot_shape(ax, shape, color='green', alpha=0.6, edgecolor=None):
    if shape.geom_type == 'Polygon':
        x, y = shape.exterior.xy
        ax.fill(x, y, alpha=alpha, fc=color, ec=edgecolor)
        for interior in shape.interiors:
            xi, yi = zip(*interior.coords)
            ax.fill(xi, yi, color='white', ec='none')
    elif shape.geom_type == 'MultiPolygon':
        for geom in shape.geoms:
            plot_shape(ax, geom, color=color, alpha=alpha, edgecolor=edgecolor)


# defining variables
phi_values = np.arange(0, 95, 5) # the mouth angle to sweep through
I_values = [] # create place to store inaccessibility values

outer_radius = 2.5 # defining the outer boundary
outer_radii = create_outer_radii(radius=outer_radius)
domain_area = outer_radii.area # compute the area of the boundary

x_vals = np.arange(-outer_radius, outer_radius + 0.01, 0.2) # x values to sweep through
y_vals = np.arange(-outer_radius, outer_radius + 0.01, 0.2) # y values to sweep through
angles = np.arange(0, 360, 4) # angle orientations to sweep through


# doing three for loops in those 4 dimentions
for phi in phi_values:
# create a C-shape at the center
    pacman1 = create_pacman(radius=1, mouth_angle_deg=phi)
    pacman_inner = create_circle(radius=0.75)
    pac_fixed = pacman1.difference(pacman_inner)

# variables as counters
    valid_shapes = []
    valid_count = 0


    for x in x_vals:
        for y in y_vals:
            for angle in angles:
                #another c shapes is introduced by doing the same pacman shape and do some translation
                pac_trial = create_pacman(radius=1, mouth_angle_deg=phi).difference(pacman_inner)
                pac_trial = rotate(pac_trial, angle, origin=(0, 0))
                pac_trial = translate(pac_trial, xoff=x, yoff=y)
# if the pacman shape is within the boundary and not null. then add it to the valid shapes
                if not pac_fixed.intersects(pac_trial) and not pac_trial.is_empty:
                    valid_shapes.append(pac_trial)
                    valid_count += 1

   # combing all valid shapes into a single shape
    accessible_union = unary_union(valid_shapes)
    accessible_area = accessible_union.intersection(outer_radii).area
    fixed_area = pac_fixed.area
    inaccessible_area = domain_area - fixed_area - accessible_area
    # find the proportion(which is the inaccessibility value)
    I = inaccessible_area / domain_area
    I_values.append(I)

    
    # plotting the shapes
    fig, ax = plt.subplots(figsize=(6, 6))
    #plot_shape(ax, outer_radii, color='lightgray', alpha=0.2)
    plot_shape(ax, accessible_union, color='green', alpha=0.4)
    plot_shape(ax, pac_fixed, color='blue', alpha=0.6)
    ax.set_title(f"Configuration phi = {phi}°, I = {I:.4f}")
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-2.5, 2.5)
    ax.set_aspect('equal')
    plt.grid(True)
    plt.savefig(f"{output_dir}/phi_{phi:02d}.png")
    plt.close()

    print(f"phi = {phi} → Valid placements: {valid_count}, I = {I:.5f}")

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

# plotting the inacessibility values versus the mouth angle
plt.figure(figsize=(8, 5))
plt.plot(phi_values, I_values, marker='o')
plt.xlabel("Mouth angle phi (degrees)")
plt.ylabel("Inaccessibility I")
plt.title("Inaccessibility I vs Mouth Angle phi")
plt.grid(True)
plt.tight_layout()
plt.show()
