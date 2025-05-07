"""
Gameplay scene for the Galaga-style game.
"""

import pygame
import sys
import random
from .scene import Scene
from .player import Player
from .enemy import Enemy, DeathAnimation
from .levels import generate_level
from . import assets
from .gameoverscene import GameOverScene
from .gameclearscene import GameClearScene

class GamePlayScene(Scene):
    def __init__(self, screen, level=1, score=0, lives=3, last_life_award=0, hp=100):
        super().__init__(screen, (0, 0, 0))
        self.level = level
        self.preserved_score = score

        # Load and scale background to screen size
        bg_image = pygame.image.load(assets.get("background1")).convert()
        self.background = pygame.transform.scale(bg_image, screen.get_size())

        self.all_sprites = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.animations = pygame.sprite.Group()

        self.font = pygame.font.SysFont("arial", 24)
        self.tip_font = pygame.font.SysFont("arial", 20)
        self.tip_start_time = pygame.time.get_ticks()
        self.tip_duration = 5000

        self.bullet_img = pygame.Surface((5, 10))
        self.bullet_img.fill((255, 255, 255))

        player_img = pygame.image.load(assets.get("player")).convert_alpha()
        player_img = pygame.transform.scale(player_img, (50, 40))

        self.player = Player(
            x=screen.get_width() // 2,
            y=screen.get_height() - 40,
            speed=5,
            image=player_img
        )
        self.player.rect.inflate_ip(-8, -4)
        self.player.hp = hp
        self.player.max_hp = 100
        self.player.score = score
        self.player.lives = lives
        self.last_life_award = last_life_award
        self.respawn_timer = None
        self.hit_flash_time = 0

        self.all_sprites.add(self.player)

        enemy_img = pygame.image.load(assets.get("enemy")).convert_alpha()
        enemy_img = pygame.transform.scale(enemy_img, (40, 35))

        enemies = generate_level(level, enemy_img, screen.get_width())
        for i, e in enumerate(enemies):
            spawn_x = 0
            spawn_y = -100
            enemy = Enemy(
                spawn_x, spawn_y,
                e['image'],
                e['speed'],
                e['entry_type'],
                entry_id=i,
                target_x=e.get("target_x", e["x"]),
                target_y=e.get("target_y", e["y"])
            )
            enemy.rect.inflate_ip(-6, -6)
            self.enemy_group.add(enemy)
            self.all_sprites.add(enemy)

        self.last_dive_time = pygame.time.get_ticks()
        self.dive_interval = 10000

        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(assets.get("gameplay"))
            pygame.mixer.music.play(-1)

    def update_scene(self):
        now = pygame.time.get_ticks()

        if now - self.last_dive_time >= self.dive_interval:
            grid_enemies = [e for e in self.enemy_group if e.is_alive_and_grid()]
            if grid_enemies:
                random.choice(grid_enemies).start_dive()
                self.last_dive_time = now

        if not self.respawn_timer:
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
        self.animations.update()

        if not self.respawn_timer and pygame.sprite.spritecollide(self.player, self.enemy_bullets, True):
            self.player.hp -= 25
            self.hit_flash_time = pygame.time.get_ticks()

        for enemy in self.enemy_group:
            if enemy.state == 'dive' and enemy.rect.colliderect(self.player.rect):
                self.player.hp -= 50
                self.animations.add(DeathAnimation(enemy.rect.centerx, enemy.rect.centery, enemy.image))
                enemy.kill()
                self.hit_flash_time = pygame.time.get_ticks()

        hits = pygame.sprite.groupcollide(self.enemy_group, self.bullet_group, True, True)
        for enemy in hits:
            self.animations.add(DeathAnimation(enemy.rect.centerx, enemy.rect.centery, enemy.image))
        if hits:
            self.player.gain_score(100 * len(hits))

        if self.player.score >= self.last_life_award + 10000:
            self.last_life_award += 10000
            self.player.lives += 1

        if len(self.enemy_group) == 0:
            if self.level < 5:
                self._next_scene = GamePlayScene(
                    self._screen,
                    level=self.level + 1,
                    score=self.player.score,
                    lives=self.player.lives,
                    last_life_award=self.last_life_award,
                    hp=self.player.hp
                )
            else:
                pygame.mixer.music.stop()
                self._next_scene = GameClearScene(self._screen, self.player.score)
            self._is_valid = False

        if self.player.hp <= 0 and self.respawn_timer is None:
            self.animations.add(DeathAnimation(self.player.rect.centerx, self.player.rect.centery, self.player.image))
            self.player.lives -= 1
            self.respawn_timer = pygame.time.get_ticks()

        if self.respawn_timer:
            if pygame.time.get_ticks() - self.respawn_timer >= 1000:
                if self.player.lives > 0:
                    original_img = pygame.image.load(assets.get("player")).convert_alpha()
                    self.player.image = pygame.transform.scale(original_img, (50, 40))
                    self.player.rect = self.player.image.get_rect(midbottom=self.player.rect.midbottom)
                    self.player.rect.inflate_ip(-8, -4)

                    self.player.hp = self.player.max_hp
                    self.player.rect.centerx = self._screen.get_width() // 2
                    self.respawn_timer = None
                else:
                    pygame.mixer.music.stop()
                    self._next_scene = GameOverScene(self._screen, self.player.score)
                    self._is_valid = False

    def draw(self):
        super().draw()
        self._screen.blit(self.background, (0, 0))  # Draw background

        if pygame.time.get_ticks() - self.hit_flash_time < 150:
            flash_overlay = pygame.Surface(self._screen.get_size())
            flash_overlay.set_alpha(80)
            flash_overlay.fill((255, 0, 0))
            self._screen.blit(flash_overlay, (0, 0))

        self.all_sprites.draw(self._screen)
        self.bullet_group.draw(self._screen)
        self.enemy_bullets.draw(self._screen)
        self.animations.draw(self._screen)

        bar_width = 100
        bar_height = 10
        bar_x = self._screen.get_width() - bar_width - 10
        bar_y = 10
        fill_width = int((self.player.hp / self.player.max_hp) * bar_width)

        pygame.draw.rect(self._screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(self._screen, (0, 255, 0), (bar_x, bar_y, fill_width, bar_height))
        pygame.draw.rect(self._screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 1)

        score_surface = self.font.render(f"Score: {self.player.score}", True, (255, 255, 255))
        self._screen.blit(score_surface, (10, 10))

        lives_surface = self.font.render(f"Lives: {self.player.lives}", True, (255, 255, 255))
        self._screen.blit(lives_surface, (10, 40))

        level_surface = self.font.render(f"Level {self.level}", True, (255, 255, 255))
        level_rect = level_surface.get_rect(center=(self._screen.get_width() // 2, 10))
        self._screen.blit(level_surface, level_rect)

        if pygame.time.get_ticks() - self.tip_start_time < self.tip_duration:
            tip_text = self.tip_font.render("A / D to move   |   W to shoot", True, (255, 255, 255))
            tip_rect = tip_text.get_rect(center=(self._screen.get_width() // 2, self._screen.get_height() - 30))
            self._screen.blit(tip_text, tip_rect)

    def process_event(self, event):
        super().process_event(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

