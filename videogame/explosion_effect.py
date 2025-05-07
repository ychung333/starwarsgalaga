"""
Explosion class for galaga.py
"""

import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, image, duration=500):
        super().__init__()
        self.original_image = image
        self.image = image.copy()
        self.rect = self.image.get_rect(center=(x, y))
        self.start_time = pygame.time.get_ticks()
        self.duration = duration

    def update(self):
        now = pygame.time.get_ticks()
        elapsed = now - self.start_time
        if elapsed >= self.duration:
            self.kill()
            return

        progress = elapsed / self.duration
        scale = max(0.1, 1 - progress)
        alpha = max(0, 255 * (1 - progress))

        new_size = (
            max(1, int(self.original_image.get_width() * scale)),
            max(1, int(self.original_image.get_height() * scale))
        )
        scaled_image = pygame.transform.smoothscale(self.original_image, new_size)
        scaled_image.set_alpha(int(alpha))
        self.image = scaled_image
        self.rect = self.image.get_rect(center=self.rect.center)

