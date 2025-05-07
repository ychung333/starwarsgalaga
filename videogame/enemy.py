"""
Enemy class for the Galaga-style game.
"""

import pygame
import random
from . import assets
from .enemy_paths import get_path

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image, speed=2, entry_type=None, entry_id=0, target_x=None, target_y=None):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.state = 'parade'
        self.direction = 1
        self.entry_type = entry_type
        self.entry_id = entry_id
        self.target_x = target_x
        self.target_y = target_y
        self.shoot_delay = random.randint(1500, 3000)
        self.last_shot_time = pygame.time.get_ticks()

        self.path_index = 0
        self.entry_duration = 120
        self.final_position = (x, y)

    def update(self, player_rect, bullet_group, bullet_image):
        if self.state == 'parade':
            self._parade()
        elif self.state == 'grid':
            self._oscillate()
        elif self.state == 'dive':
            self._dive()

        self._maybe_shoot(bullet_group, bullet_image)

    def _parade(self):
        x, y = get_path(self.entry_type, self.entry_id, self.path_index, self.target_x, self.target_y)
        self.rect.center = (x, y)
        self.path_index += 1
        if self.path_index >= self.entry_duration:
            self.state = 'grid'

    def _oscillate(self):
        self.rect.x += self.speed * self.direction
        if self.rect.left <= 0 or self.rect.right >= 800:
            self.direction *= -1

    def _dive(self):
        self.rect.y += 6
        if self.rect.top > 600:
            self.kill()

    def _maybe_shoot(self, bullet_group, bullet_image):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time > self.shoot_delay:
            bullet = EnemyBullet(self.rect.centerx, self.rect.bottom, bullet_image)
            bullet_group.add(bullet)
            self.last_shot_time = now
            self.shoot_delay = random.randint(1500, 3000)

            try:
                sound = pygame.mixer.Sound(assets.get("enemy_fire"))
                sound.set_volume(0.03)
                sound.play()
            except pygame.error:
                print("Could not play enemy_fire.wav")

    def is_alive_and_grid(self):
        return self.alive() and self.state == 'grid'

    def start_dive(self):
        if self.state == 'grid':
            self.state = 'dive'
            try:
                dive_sound = pygame.mixer.Sound(assets.get("dive"))
                dive_sound.set_volume(0.3)
                pygame.mixer.Channel(0).play(dive_sound)
            except pygame.error:
                print("Could not play dive.wav")


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

