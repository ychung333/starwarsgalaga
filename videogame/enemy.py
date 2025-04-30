"""
Enemy class for the Galaga-style game.
"""

import pygame
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image, speed=2):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.state = 'parade'  # 'grid', 'dive', etc.
        self.direction = 1
        self.shoot_delay = random.randint(1500, 3000)
        self.last_shot_time = pygame.time.get_ticks()

    def update(self, player_rect, bullet_group, bullet_image):
        if self.state == 'parade':
            self._parade()
        elif self.state == 'grid':
            self._oscillate()
        elif self.state == 'dive':
            self._dive(player_rect)
        self._maybe_shoot(bullet_group, bullet_image)

    def _parade(self):
        self.rect.y += self.speed
        if self.rect.y >= 100:  # Arbitrary y-pos to stop
            self.state = 'grid'

    def _oscillate(self):
        self.rect.x += self.speed * self.direction
        if self.rect.left <= 0 or self.rect.right >= 800:
            self.direction *= -1

    def _dive(self, player_rect):
        dx = player_rect.centerx - self.rect.centerx
        dy = player_rect.centery - self.rect.centery
        dist = max(1, (dx ** 2 + dy ** 2) ** 0.5)
        self.rect.x += int(3 * dx / dist)
        self.rect.y += int(3 * dy / dist)

    def _maybe_shoot(self, bullet_group, bullet_image):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time > self.shoot_delay:
            bullet = EnemyBullet(self.rect.centerx, self.rect.bottom, bullet_image)
            bullet_group.add(bullet)
            self.last_shot_time = now
            self.shoot_delay = random.randint(1500, 3000)


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
