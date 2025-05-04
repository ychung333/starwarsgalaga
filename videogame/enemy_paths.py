"""
Defines different enemy entry animations (parade paths) used when enemies fly onto the screen at the start of each level.
"""

import math

def straight_entry(enemy):
    """Simple straight-down descent."""
    enemy.rect.y += enemy.speed

def sine_entry(enemy):
    """Wavy left-right motion while descending."""
    enemy.rect.y += enemy.speed
    enemy.rect.x = enemy.entry_origin_x + int(40 * math.sin(enemy.entry_progress / 10))

def zigzag_entry(enemy):
    """Sharp left-right zigzag descent."""
    enemy.rect.y += enemy.speed
    enemy.rect.x += enemy.direction * 4
    if enemy.entry_progress % 20 == 0:
        enemy.direction *= -1

def spiral_entry(enemy):
    """Circular spiral descent inward."""
    radius = 40 - enemy.entry_progress // 5
    angle = enemy.entry_progress / 10
    enemy.rect.x = enemy.entry_origin_x + int(radius * math.cos(angle))
    enemy.rect.y += enemy.speed

def curve_entry(enemy):
    """Bezier-like curved descent."""
    t = enemy.entry_progress / 60
    enemy.rect.x = enemy.entry_origin_x + int(60 * (1 - t) * t * 2)
    enemy.rect.y += enemy.speed

