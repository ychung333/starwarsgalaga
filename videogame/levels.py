"""
Defines enemy wave patterns and level difficulty progression.
"""

import random


def generate_level(level_number, enemy_image, screen_width):
    """
    Generate a list of enemy spawn positions for the given level.
    Higher levels can have more enemies and faster movement.
    """
    enemy_count = min(20 + level_number * 5, 80)
    spacing_x = 40
    spacing_y = 40
    cols = min(enemy_count // 4, 10)
    rows = enemy_count // cols

    enemies = []
    start_x = (screen_width - (cols * spacing_x)) // 2
    for row in range(rows):
        for col in range(cols):
            x = start_x + col * spacing_x
            y = 50 + row * spacing_y
            speed = 2 + level_number * 0.2
            enemies.append({
                'x': x,
                'y': y,
                'speed': speed,
                'image': enemy_image
            })

    return enemies
