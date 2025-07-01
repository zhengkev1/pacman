import math

def write_pacman_sector(f, center_x, center_y, radius=1.0, mouth_angle_deg=45, tag_base=1000):
    angle_start = math.radians(mouth_angle_deg / 2)
    angle_end = 2 * math.pi - angle_start
    segments = 50

    point_ids = []
    f.write(f"\n// Pac-Man at ({center_x}, {center_y})\n")
    f.write(f"Point({tag_base}) = {{{center_x}, {center_y}, 0, 0.01}};\n")
    point_ids.append(tag_base)
    tag = tag_base + 1

    for i, a in enumerate([angle_start + (angle_end - angle_start) * j / segments for j in range(segments + 1)]):
        x = center_x + radius * math.cos(a)
        y = center_y + radius * math.sin(a)
        f.write(f"Point({tag}) = {{{x}, {y}, 0, 0.01}};\n")
        point_ids.append(tag)
        tag += 1

    line_ids = []
    for i in range(1, len(point_ids) - 1):
        f.write(f"Line({tag}) = {{{point_ids[i]}, {point_ids[i + 1]}}};\n")
        line_ids.append(tag)
        tag += 1

    # Line from center to start
    f.write(f"Line({tag}) = {{{point_ids[0]}, {point_ids[1]}}};\n")
    line_ids = [tag] + line_ids
    tag += 1
    # Line from last arc point to center
    f.write(f"Line({tag}) = {{{point_ids[-1]}, {point_ids[0]}}};\n")
    line_ids.append(tag)
    tag += 1

    loop_id = tag
    f.write(f"Curve Loop({loop_id}) = {{{', '.join(map(str, line_ids))}}};\n")
    tag += 1
    surface_id = tag
    f.write(f"Plane Surface({surface_id}) = {{{loop_id}}};\n")

    return surface_id, tag + 1  # return next available tag

# === Write the geo file ===
with open("pacman_access.geo", "w") as f:
    f.write("SetFactory(\"OpenCASCADE\");\n")
    next_tag = 1

    # Add fixed Pac-Man
    fixed_surface, next_tag = write_pacman_sector(f, 0, 0, radius=1.0, mouth_angle_deg=45, tag_base=next_tag)

    # Add trial Pac-Men
    offsets = [-1, 0, 1]
    for i, dx in enumerate(offsets):
        for j, dy in enumerate(offsets):
            cx, cy = dx * 1.5, dy * 1.5
            _, next_tag = write_pacman_sector(f, cx, cy, radius=1.0, mouth_angle_deg=45, tag_base=next_tag)

    f.write(f"Physical Surface(\"fixed\") = {{{fixed_surface}}};\n")
