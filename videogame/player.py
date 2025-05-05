"""
Player class for the Galaga-style game.
"""

import pygame
from . import assets

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.speed = speed
        self.lives = 3
        self.score = 0
        self.shoot_cooldown = 300  # milliseconds
        self.last_shot_time = pygame.time.get_ticks()

    def move(self, keys, screen_width):
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 0:
            self.rect.x -= self.speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < screen_width:
            self.rect.x += self.speed

    def shoot(self, bullet_group, bullet_image):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.shoot_cooldown:
            bullet = Bullet(self.rect.centerx, self.rect.top, bullet_image)
            bullet_group.add(bullet)
            self.last_shot_time = current_time

            # 🔊 Play player fire sound at low volume
            try:
                sound = pygame.mixer.Sound(assets.get("player_fire"))
                sound.set_volume(0.03)
                sound.play()
            except pygame.error:
                print("Could not play player_fire.wav")

    def update(self, keys, screen_width, bullet_group, bullet_image):
        self.move(keys, screen_width)
        if keys[pygame.K_w]:  # Fire with W key
            self.shoot(bullet_group, bullet_image)

    def lose_life(self):
        self.lives -= 1

    def gain_score(self, points):
        self.score += points
        if self.score // 10000 > (self.score - points) // 10000:
            self.lives += 1


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()


