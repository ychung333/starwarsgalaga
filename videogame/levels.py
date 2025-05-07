"""
Level generator for Galaga-style waves.
"""
import random

def generate_level(level, enemy_image, screen_width):
    enemies = []

    enemy_width = enemy_image.get_width()
    enemy_height = enemy_image.get_height()

    enemies_per_level = 20 + (level - 1) * 5
    enemies_per_row = 10
    rows = (enemies_per_level + enemies_per_row - 1) // enemies_per_row  # ceiling division

    spacing_x = enemy_width  # 1 block distance horizontally
    spacing_y = enemy_height + 20  # vertical spacing

    total_row_width = enemies_per_row * enemy_width + (enemies_per_row - 1) * spacing_x
    start_x = (screen_width - total_row_width) // 2

    for i in range(enemies_per_level):
        row = i // enemies_per_row
        col = i % enemies_per_row

        x = start_x + col * (enemy_width + spacing_x)
        y = 100 + row * spacing_y

        enemy_dict = {
            "x": x,
            "y": y,
            "image": enemy_image,
            "speed": 2 + level * 0.2,
            "entry_type": "straight"
        }
        enemies.append(enemy_dict)

    return enemies


