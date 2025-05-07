"""
Level generator for Galaga-style waves.
"""

import random

def generate_level(level, enemy_image, screen_width):
    enemies = []

    enemy_width = enemy_image.get_width()
    enemy_height = enemy_image.get_height()

    enemies_per_level = 20 + (level - 1) * 5

    # Fixed rows and entry_type for each level
    if level == 1:
        rows = 2
        entry_type = "to_grid"
    elif level == 2:
        rows = 3
        entry_type = "to_grid"
    elif level == 3:
        rows = 3
        entry_type = "spiral"
    elif level == 4:
        rows = 4
        entry_type = "to_grid"
    elif level == 5:
        rows = 4
        entry_type = "rise"
    else:
        rows = (enemies_per_level + 9) // 10
        entry_type = "sine"

    cols = (enemies_per_level + rows - 1) // rows  # Ceiling division

    spacing_x = enemy_width + 20
    spacing_y = enemy_height + 20

    total_grid_width = cols * enemy_width + (cols - 1) * 20
    start_x = (screen_width - total_grid_width) // 2
    top_margin = 100

    for i in range(enemies_per_level):
        row = i // cols
        col = i % cols

        x = start_x + col * spacing_x
        y = top_margin + row * spacing_y

        enemy_dict = {
            "x": x,
            "y": y,
            "image": enemy_image,
            "speed": 2 + level * 0.2,
            "entry_type": entry_type
        }

        if entry_type in ["to_grid", "rise"]:
            enemy_dict["target_x"] = x
            enemy_dict["target_y"] = y

        enemies.append(enemy_dict)

    return enemies


