"""
Level generator for Galaga-style waves.
"""

def generate_level(level, enemy_image, screen_width):
    enemies = []
    columns = min(5 + level, 10)  # gradually increase columns up to max 10
    rows = 4
    spacing_x = screen_width // (columns + 1)
    spacing_y = 50

    for row in range(rows):
        for col in range(columns):
            x = spacing_x * (col + 1)
            y = spacing_y * (row + 1)
            enemies.append({
                'x': x,
                'y': y,
                'image': enemy_image,
                'speed': 1 + (level * 0.1)
            })

    return enemies

