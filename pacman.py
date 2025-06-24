import math
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point
from shapely.affinity import rotate, translate
from shapely.ops import unary_union

def create_pacman(radius=1, mouth_angle_deg=60, segments=100):
    theta = math.radians(mouth_angle_deg / 2)
    arc = [(radius * math.cos(a), radius * math.sin(a))
           for a in np.linspace(theta, 2 * math.pi - theta, segments)]
    return Polygon([(0, 0)] + arc + [(0, 0)])


def plot_shape(ax, shape, color='green', alpha=0.6, edgecolor='black'):
    if shape.geom_type == 'Polygon':
        x, y = shape.exterior.xy
        ax.fill(x, y, alpha=alpha, fc=color, ec=edgecolor)
    elif shape.geom_type == 'MultiPolygon':
        for geom in shape.geoms:
            plot_shape(ax, geom, color=color, alpha=alpha, edgecolor=edgecolor)


pacman1 = create_pacman()

coords =[(-0.5,-0.5), (-0.5, 0.5),(0.5, +0.5),(0.5, -0.5),(-0.5,-0.5)]
polygon = Polygon(coords)

x_vals = np.arange(-1, 2.5, 0.2)
y_vals = np.arange(-2.5, 2.5, 0.2)
angles = np.arange(0, 360, 10)

point = Point (0.2,0.0)

valid_shapes = []
valid_count = 0

for x in x_vals:
    
    for y in y_vals:
        for angle in angles:
            pac2 = create_pacman()
            pac2 = rotate(pac2, angle, origin=(0, 0))
            pac2 = translate(pac2, xoff=x, yoff=y)

            if not pacman1.intersects(pac2):
                valid_shapes.append(pac2)
                valid_count += 1


accessible_union = unary_union(valid_shapes)




print(f"Total accessible union area: {accessible_union.area:.5f}")
print(f"Total valid placements: {valid_count}")

fig, ax = plt.subplots(figsize=(8, 8))
plot_shape(ax, accessible_union, color='green', alpha=0.4)
plot_shape(ax, pacman1, color='yellow', alpha=0.95)
plot_shape (ax, polygon, color = 'red', alpha = 0.7)

ax.set_title("Reachable Area (Green) vs Fixed Pac-Man (Yellow)")
ax.set_aspect('equal')
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
plt.grid(True)
plt.show()
