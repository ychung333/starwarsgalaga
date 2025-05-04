"""
Level generator for Galaga-style waves.
"""
def generate_level(level, enemy_image, screen_width):

    enemies = []

    # Determine total enemies: 20 + 5 * (level - 1)
    total_enemies = 20 + (level - 1) * 5

    # Set grid size based on enemy count
    cols = min(10, total_enemies)  # Max 10 columns
    rows = (total_enemies + cols - 1) // cols  # Round up to fit all enemies

    # Positioning settings
    min_x_margin = 40
    spacing_x = max((screen_width - 2 * min_x_margin) // cols, 60)  # at least 60px apart
    spacing_y = 60

    # Create enemy positions
    for row in range(rows):
        for col in range(cols):
            if len(enemies) >= total_enemies:
                break
            x = min_x_margin + col * spacing_x
            y = 60 + row * spacing_y
            enemies.append({
                'x': x,
                'y': y,
                'image': enemy_image,
                'speed': 2 + 0.2 * level
            })

    return enemies


