import math
import time
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from shapely.affinity import rotate, translate
from shapely.ops import unary_union


def create_pacman(radius=1, mouth_angle_deg=30, segments=100):
    theta = math.radians(mouth_angle_deg / 2)
    arc = [(radius * math.cos(a), radius * math.sin(a))
           for a in np.linspace(theta, 2 * math.pi - theta, segments)]
    return Polygon([(0, 0)] + arc + [(0, 0)])

def create_circle(radius=0.75, segments=100):
    arc = [(radius * math.cos(a), radius * math.sin(a))
           for a in np.linspace(0, 2 * math.pi, segments)]
    return Polygon([(0, 0)] + arc + [(0, 0)])

def create_outer_radii(radius=2.5, segments=100):
    arc = [(radius * math.cos(a), radius * math.sin(a))
           for a in np.linspace(0, 2 * math.pi, segments)]
    return Polygon([(0, 0)] + arc + [(0, 0)])


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


mouth_angle = 25
outer_radius = 2.5  


pacman1 = create_pacman(radius=1, mouth_angle_deg=mouth_angle)
circle1 = create_circle(radius=0.75)
pac_fixed = pacman1.difference(circle1)
#pac_fixed = pacman1

outer_radii = create_outer_radii(radius=outer_radius)
domain_area = math.pi * outer_radius**2


x_vals = np.arange(-outer_radius, outer_radius + 0.01, 0.1)
y_vals = np.arange(-outer_radius, outer_radius + 0.01, 0.1)
angles = np.arange(0,360,10)

valid_shapes = []
valid_count = 0

for x in x_vals:
    for y in y_vals:
        for angle in angles:
            pac_trial = create_pacman(radius=1, mouth_angle_deg=mouth_angle).difference(circle1)
            #pac_trial = create_pacman(radius=1, mouth_angle_deg=mouth_angle)
            pac_trial = rotate(pac_trial, angle, origin=(0, 0))
            pac_trial = translate(pac_trial, xoff=x, yoff=y)

            # Cut to within circular boundary
            # clipped = pac_trial.intersection(outer_radii)

            if not pac_fixed.intersects(pac_trial) and not pac_trial.is_empty:
                valid_shapes.append(pac_trial)
                valid_count += 1


accessible_union = unary_union(valid_shapes)
accessible_area = accessible_union.area
fixed_pacman_area = pac_fixed.area
inaccessible_area = domain_area - fixed_pacman_area - accessible_area
I = inaccessible_area / domain_area


print(f"Total valid placements: {valid_count}")
print(f"Total accessible area (sum): {accessible_area:.5f}")
print(f"Total inaccessible area: {inaccessible_area:.5f}")
print(f"Inaccessibility index I = {I:.5f}")

fig, ax = plt.subplots(figsize=(8, 8))
#for shape in valid_shapes:
plot_shape(ax, accessible_union, color='green', alpha=0.3)
plot_shape(ax, pac_fixed, color='blue', alpha=0.6)

ax.set_title("Reachable Area (green) vs Fixed Pac-Man (blue)")
ax.set_xlim(-2.5, 2.5)
ax.set_ylim(-2.5, 2.5)
ax.set_aspect('equal')
plt.grid(True)
plt.show()
