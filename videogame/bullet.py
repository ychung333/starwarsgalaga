"""
Bullet class for reuse if separating from Player or Enemy
"""

import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, image, direction=-1, speed=10):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed * direction

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0 or self.rect.top > 600:
            self.kill()
