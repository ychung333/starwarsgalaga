"""
Game Clear scene for when the player completes the final level.
"""

import pygame
import sys
from .scene import Scene
from . import assets
from .leaderboardscene import LeaderboardScene
from .leaderboard import add_score, is_high_score

class GameClearScene(Scene):
    def __init__(self, screen, score):
        super().__init__(screen, (0, 0, 0))  # Black background
        self._score = score

        self.title_font = pygame.font.SysFont("arial", 48)
        self.text_font = pygame.font.SysFont("arial", 28)

        self.title_text = self.title_font.render("🎉 Congratulations! 🎉", True, (255, 255, 0))
        self.message_text = self.text_font.render(
            "You cleared all levels!", True, (255, 255, 255)
        )
        self.instruction_text = self.text_font.render(
            "Press ENTER to view leaderboard, ESC to quit", True, (200, 200, 200)
        )

        # 🎵 Play win music using asset system
        pygame.mixer.music.stop()
        pygame.mixer.music.load(assets.get("win"))
        pygame.mixer.music.play()

    def draw(self):
        super().draw()
        w, h = self._screen.get_width(), self._screen.get_height()

        # Calculate vertical stacking
        spacing = 50
        center_y = h // 2

        title_rect = self.title_text.get_rect(center=(w // 2, center_y - spacing))
        message_rect = self.message_text.get_rect(center=(w // 2, center_y))
        instruction_rect = self.instruction_text.get_rect(center=(w // 2, center_y + spacing))

        self._screen.blit(self.title_text, title_rect)
        self._screen.blit(self.message_text, message_rect)
        self._screen.blit(self.instruction_text, instruction_rect)

    def process_event(self, event):
        super().process_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if is_high_score(self._score):
                    add_score(self._score)
                self._next_scene = LeaderboardScene(self._screen)
                self._is_valid = False
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

