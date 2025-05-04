"""
Level generator for Galaga-style waves.
"""
import random

def generate_level(level, enemy_image, screen_width):
    enemies = []

    rows = 3 + (level % 3)       # 3 to 5 rows
    cols = min(6 + level * 2, 10)  # max 10 columns

    min_x_margin = 40
    spacing_x = max((screen_width - 2 * min_x_margin) // cols, 60)
    spacing_y = 50

    entry_types = ["straight", "sine", "zigzag", "spiral", "curve"]

    for row in range(rows):
        for col in range(cols):
            x = min_x_margin + col * spacing_x
            y = -random.randint(30, 150)  # start off-screen

            enemy_dict = {
                "x": x,
                "y": y,
                "image": enemy_image,
                "speed": 2 + level * 0.2,
                "entry_type": random.choice(entry_types)
            }
            enemies.append(enemy_dict)

    return enemies

