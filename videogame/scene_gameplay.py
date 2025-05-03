"""
Gameplay scene for the Galaga-style game.
"""

import pygame
import sys
from .scene import Scene
from .player import Player
from .enemy import Enemy
from .levels import generate_level
from . import assets
from .gameoverscene import GameOverScene
from .gameclearscene import GameClearScene

class GamePlayScene(Scene):
    def __init__(self, screen, level=1, score=0):
        super().__init__(screen, (0, 0, 0))  # Black background
        print(f"Entered GamePlayScene - Level {level}")

        self.level = level
        self.preserved_score = score

        self.all_sprites = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()

        self.font = pygame.font.SysFont("arial", 24)

        # Placeholder bullet image
        self.bullet_img = pygame.Surface((5, 10))
        self.bullet_img.fill((255, 255, 255))

        # Placeholder player image
        player_img = pygame.Surface((40, 30))
        player_img.fill((0, 255, 0))
        self.player = Player(
            x=screen.get_width() // 2,
            y=screen.get_height() - 40,
            speed=5,
            image=player_img
        )
        self.player.hp = 100
        self.player.max_hp = 100
        self.player.score = score
        self.hit_flash_time = 0

        self.all_sprites.add(self.player)

        # Placeholder enemy image
        enemy_img = pygame.Surface((30, 30))
        enemy_img.fill((255, 0, 0))
        enemies = generate_level(level, enemy_img, screen.get_width())
        for e in enemies:
            enemy = Enemy(e['x'], e['y'], e['image'], e['speed'])
            self.enemy_group.add(enemy)
            self.all_sprites.add(enemy)

    def update_scene(self):
        keys = pygame.key.get_pressed()
        self.player.update(
            keys,
            self._screen.get_width(),
            self.bullet_group,
            self.bullet_img
        )

        for enemy in self.enemy_group:
            enemy.update(self.player.rect, self.enemy_bullets, self.bullet_img)

        self.bullet_group.update()
        self.enemy_bullets.update()

        # Check if player is hit by enemy bullets
        if pygame.sprite.spritecollide(self.player, self.enemy_bullets, True):
            self.player.hp -= 25
            self.hit_flash_time = pygame.time.get_ticks()
            print("Player hit! HP:", self.player.hp)

        # Collision detection: player bullets hit enemies
        hits = pygame.sprite.groupcollide(self.enemy_group, self.bullet_group, True, True)
        if hits:
            self.player.gain_score(50 * len(hits))

        # End level if all enemies are gone
        if len(self.enemy_group) == 0:
            if self.level < 5:
                self._next_scene = GamePlayScene(self._screen, level=self.level + 1, score=self.player.score)
            else:
                self._next_scene = GameClearScene(self._screen, self.player.score)
            self._is_valid = False

        # Trigger Game Over Scene if HP is 0 or less
        if self.player.hp <= 0:
            self._next_scene = GameOverScene(self._screen, self.player.score)
            self._is_valid = False

    def draw(self):
        super().draw()

        # Flash red effect if hit recently
        if pygame.time.get_ticks() - self.hit_flash_time < 150:
            flash_overlay = pygame.Surface(self._screen.get_size())
            flash_overlay.set_alpha(80)
            flash_overlay.fill((255, 0, 0))
            self._screen.blit(flash_overlay, (0, 0))

        self.all_sprites.draw(self._screen)
        self.bullet_group.draw(self._screen)
        self.enemy_bullets.draw(self._screen)

        # Draw HP bar at top-right
        bar_width = 100
        bar_height = 10
        bar_x = self._screen.get_width() - bar_width - 10
        bar_y = 10
        fill_width = int((self.player.hp / self.player.max_hp) * bar_width)

        pygame.draw.rect(self._screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))  # red bg
        pygame.draw.rect(self._screen, (0, 255, 0), (bar_x, bar_y, fill_width, bar_height))  # green hp
        pygame.draw.rect(self._screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 1)  # white border

        # Draw score at top-left
        score_surface = self.font.render(f"Score: {self.player.score}", True, (255, 255, 255))
        self._screen.blit(score_surface, (10, 10))

    def process_event(self, event):
        super().process_event(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()


