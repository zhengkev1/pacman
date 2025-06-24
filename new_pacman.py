import math
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point
from shapely.affinity import rotate, translate
from shapely.ops import unary_union

def create_pacman(radius=1, mouth_angle_deg=30, segments=100):
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

#pac3 = pacman1.difference(polygon)

def create_circle (radius = 0.75, segments= 100):
    theta = 0
    arc = [(radius * math.cos(a), radius * math.sin(a))
           for a in np.linspace(theta, 2 * math.pi - theta, segments)]
    return Polygon([(0, 0)] + arc + [(0, 0)])

def create_outer_radii (radius = 1, segments= 100):
    theta = 0
    arc = [(radius * math.cos(a), radius * math.sin(a))
           for a in np.linspace(theta, 2 * math.pi - theta, segments)]
    return Polygon([(0, 0)] + arc + [(0, 0)])


circle1 = create_circle()
pac4 = pacman1.difference(circle1)
outer_radii= create_outer_radii()

circle1 = create_circle()

x_vals = np.arange(-1, 2.5, 0.2)
y_vals = np.arange(-2.5, 2.5, 0.2)
angles = np.arange(0, 360, 2)

point = Point (0.2,0.0)

valid_shapes = []
valid_count = 0

for x in x_vals:
    
    for y in y_vals:
        for angle in angles:
            pac2 = pac4
            pac2 = rotate(pac2, angle, origin=(0, 0))
            pac2 = translate(pac2, xoff=x, yoff=y)

            if not pac4.intersects(pac2):
                valid_shapes.append(pac2)
                valid_count += 1


accessible_union = unary_union(valid_shapes)

accessible_area_inside = (outer_radii.intersection(accessible_union))
inaccesible_area = outer_radii.area - pac4.area-accessible_area_inside.area


print(f"Total accessible union area: {accessible_union.area:.5f}")
print(f"Total valid placements: {valid_count}")
print(f"Total inaccessible union area: {inaccesible_area:.5f}")

fig, ax = plt.subplots(figsize=(8, 8))
plot_shape(ax, accessible_union, color='green', alpha=0.4)
#plot_shape(ax, pacman1, color='yellow', alpha=0.95)
#plot_shape (ax, pac3, color = 'red', alpha = 0.7)
plot_shape (ax, pac4, color = 'blue', alpha = 0.5)

ax.set_title("Reachable Area (Green) vs Fixed Pac-Man (Yellow)")
ax.set_aspect('equal')
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
plt.grid(True)
plt.show()
