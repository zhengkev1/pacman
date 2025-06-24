import math
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from shapely.affinity import rotate, translate
from shapely.ops import unary_union

def create_pacman(radius=1, mouth_angle_deg=5, segments=100):
    theta = math.radians(mouth_angle_deg / 2)
    arc = [(radius * math.cos(a), radius * math.sin(a))
           for a in np.linspace(theta, 2 * math.pi - theta, segments)]
    return Polygon([(0, 0)] + arc + [(0, 0)])

def create_circle(radius=0.75, segments=100):
    arc = [(radius * math.cos(a), radius * math.sin(a))
           for a in np.linspace(0, 2 * math.pi, segments)]
    return Polygon([(0, 0)] + arc + [(0, 0)])

def create_outer_radii(radius=1, segments=100):
    arc = [(radius * math.cos(a), radius * math.sin(a))
           for a in np.linspace(0, 2 * math.pi, segments)]
    return Polygon([(0, 0)] + arc + [(0, 0)])

def plot_shape(ax, shape, color='green', alpha=0.6, edgecolor='black'):
    if shape.geom_type == 'Polygon':
        x, y = shape.exterior.xy
        ax.fill(x, y, alpha=alpha, fc=color, ec=edgecolor)
    elif shape.geom_type == 'MultiPolygon':
        for geom in shape.geoms:
            plot_shape(ax, geom, color=color, alpha=alpha, edgecolor=edgecolor)


phi_values = np.arange(0, 95, 2)        
I_values = []                           
outer_radius = 1.0                      
outer_radii = create_outer_radii(radius=outer_radius)

x_vals = np.arange(-1, 2.5, 0.2)
y_vals = np.arange(-2.5, 2.5, 0.2)
angles = np.arange(0, 360, 5)


for phi in phi_values:
    pacman1 = create_pacman(radius=outer_radius, mouth_angle_deg=phi)
    circle1 = create_circle(radius=0.75)
    pac4 = pacman1.difference(circle1)

    valid_shapes = []
    valid_count = 0

    for x in x_vals:
        for y in y_vals:
            for angle in angles:
                pac2 = rotate(pac4, angle, origin=(0, 0))
                pac2 = translate(pac2, xoff=x, yoff=y)

                if not pac4.intersects(pac2):
                    valid_shapes.append(pac2)
                    valid_count += 1

    accessible_union = unary_union(valid_shapes)
    accessible_area_inside = outer_radii.intersection(accessible_union)
    inaccessible_area = outer_radii.area - pac4.area - accessible_area_inside.area

    I = inaccessible_area / (math.pi * outer_radius**2)
    I_values.append(I)

    print(f"phi = {phi:2d}°, Valid placements = {valid_count:4d}, I = {I:.5f}")


plt.figure(figsize=(8, 6))
plt.plot(phi_values, I_values, marker='o')
plt.xlabel("Mouth Angle φ (degrees)")
plt.ylabel("Inaccessibility I (normalized)")
plt.title("Inaccessibility I vs Pac-Man Mouth Angle φ")
plt.grid(True)
plt.show()
