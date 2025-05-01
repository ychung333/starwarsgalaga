"""
Gameplay scene for the Galaga-style game.
"""

import pygame
from .scene import Scene
from .player import Player
from .enemy import Enemy
from .levels import generate_level
from . import assets

class GamePlayScene(Scene):
    def __init__(self, screen):
        super().__init__(screen, (0, 0, 0))  # Black background
        self.all_sprites = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()

        # Load player (placeholder surface)
        player_img = pygame.Surface((40, 30))  # Replace with assets.get("player_image") later
        player_img.fill((0, 255, 0))
        self.player = Player(x=screen.get_width() // 2, y=screen.get_height() - 40, speed=5, image=player_img)
        self.all_sprites.add(self.player)

        # Load enemies (placeholder surface)
        enemy_img = pygame.Surface((30, 30))  # Replace with assets.get("enemy_image") later
        enemy_img.fill((255, 0, 0))
        enemies = generate_level(1, enemy_img, screen.get_width())
        for e in enemies:
            enemy = Enemy(e['x'], e['y'], e['image'], e['speed'])
            self.enemy_group.add(enemy)
            self.all_sprites.add(enemy)

    def update_scene(self):
        keys = pygame.key.get_pressed()
        self.player.update(keys, self._screen.get_width(), self.bullet_group, None)

        self.all_sprites.update()
        self.bullet_group.update()
        self.enemy_bullets.update()

        # Collision detection
        hits = pygame.sprite.groupcollide(self.enemy_group, self.bullet_group, True, True)
        if hits:
            self.player.gain_score(50 * len(hits))

        # End level if all enemies are gone
        if len(self.enemy_group) == 0:
            self._is_valid = False

    def draw(self):
        super().draw()
        self.all_sprites.draw(self._screen)
        self.bullet_group.draw(self._screen)
        self.enemy_bullets.draw(self._screen)

    def process_event(self, event):
        super().process_event(event)
