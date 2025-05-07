"""
Defines different enemy entry animations (parade paths) used when enemies fly onto the screen at the start of each level.
"""

import math

def sine_path(index, frame):
    offset = (index % 10 - 5) * 40
    x = 400 + offset + 100 * math.sin(0.05 * frame)
    y = frame * 2
    return x, y

def zigzag_path(index, frame):
    offset = (index % 10 - 5) * 40
    x = 400 + offset + 80 * ((frame // 30) % 2 * 2 - 1) * math.sin(0.1 * frame)
    y = frame * 2
    return x, y

def spiral_path(index, frame):
    base_angle = index * 15
    angle = 0.1 * frame + math.radians(base_angle)
    radius = 50 + frame * 0.5
    x = 400 + radius * math.cos(angle)
    y = 100 + radius * math.sin(angle)
    return x, y

def bounce_path(index, frame):
    offset = (index % 10 - 5) * 40
    x = 400 + offset + 100 * math.sin(0.1 * frame)
    y = 100 + abs((frame % 100) - 50) * 2
    return x, y

def split_loop_path(index, frame):
    spread = (index % 10 - 5) * 30
    angle = frame * 3 + spread
    radius = 100 + (frame % 60)
    x = 400 + radius * math.cos(math.radians(angle))
    y = 100 + radius * math.sin(math.radians(angle))
    return x, y

def rise_path(index, frame, target_x, target_y):
    start_x = -50
    start_y = 700
    duration = 120
    t = min(frame / duration, 1)
    x = start_x + (target_x - start_x) * t
    y = start_y + (target_y - start_y) * t
    return x, y

def to_grid_path(index, frame, target_x, target_y):
    # Enemies start above screen, drift slightly based on index
    start_x = 400 + (index % 10 - 5) * 60
    start_y = -50
    duration = 120
    t = min(frame / duration, 1)
    x = start_x + (target_x - start_x) * t
    y = start_y + (target_y - start_y) * t
    return x, y

def get_path(entry_type, index, frame, target_x=None, target_y=None):
    if entry_type == "rise":
        return rise_path(index, frame, target_x, target_y)
    elif entry_type == "to_grid":
        return to_grid_path(index, frame, target_x, target_y)
    elif entry_type == "sine":
        return sine_path(index, frame)
    elif entry_type == "zigzag":
        return zigzag_path(index, frame)
    elif entry_type == "spiral":
        return spiral_path(index, frame)
    elif entry_type == "bounce":
        return bounce_path(index, frame)
    elif entry_type == "split-loop":
        return split_loop_path(index, frame)
    else:
        return sine_path(index, frame)

