"""
Enemy class for the Galaga-style game.
"""

import pygame
import random
from . import enemy_paths
import math

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image, speed=2, entry_type="straight"):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.state = 'parade'  # 'parade', 'grid', 'dive'
        self.direction = 1
        self.shoot_delay = random.randint(1500, 3000)
        self.last_shot_time = pygame.time.get_ticks()

        self.entry_type = entry_type
        self.entry_origin_x = x
        self.entry_progress = 0

    def update(self, player_rect, bullet_group, bullet_image):
        if self.state == 'parade':
            self._parade()
        elif self.state == 'grid':
            self._oscillate()
        elif self.state == 'dive':
            self._dive()

        self._maybe_shoot(bullet_group, bullet_image)

    def _parade(self):
        self.entry_progress += 1

        entry_funcs = {
            "straight": enemy_paths.straight_entry,
            "sine": enemy_paths.sine_entry,
            "zigzag": enemy_paths.zigzag_entry,
            "spiral": enemy_paths.spiral_entry,
            "curve": enemy_paths.curve_entry
        }

        func = entry_funcs.get(self.entry_type, enemy_paths.straight_entry)
        func(self)

        if self.rect.y >= 100:
            self.state = 'grid'

    def _oscillate(self):
        self.rect.x += self.speed * self.direction

        # ✅ Wall boundary + bounce fix
        if self.rect.left <= 0:
            self.rect.left = 0
            self.direction = 1
        elif self.rect.right >= 800:
            self.rect.right = 800
            self.direction = -1

    def _dive(self):
        self.rect.y += self.speed * 3
        if self.rect.top > 600:
            self.kill()

    def _maybe_shoot(self, bullet_group, bullet_image):
        if self.state == 'dive':
            return
        now = pygame.time.get_ticks()
        if now - self.last_shot_time > self.shoot_delay:
            bullet = EnemyBullet(self.rect.centerx, self.rect.bottom, bullet_image)
            bullet_group.add(bullet)
            self.last_shot_time = now
            self.shoot_delay = random.randint(1500, 3000)

    def start_dive(self):
        if self.state == 'grid':
            self.state = 'dive'

    def is_alive_and_grid(self):
        return self.state == 'grid'

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(midtop=(x, y))
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.kill()

