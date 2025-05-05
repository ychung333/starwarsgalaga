"""
Game Over scene for the Galaga-style game.
"""

import pygame
import sys
from .scene import Scene
from .leaderboardscene import LeaderboardScene
from .leaderboard import is_high_score, add_score

class GameOverScene(Scene):
    def __init__(self, screen, score):
        super().__init__(screen, (0, 0, 0))
        self.font = pygame.font.SysFont("arial", 48)
        self.text_font = pygame.font.SysFont("arial", 28)
        self.small_font = pygame.font.SysFont("arial", 24)

        self.game_over_text = self.font.render("Game Over", True, (255, 0, 0))
        self.message_text = self.text_font.render("Better luck next time!", True, (255, 255, 255))
        self.instruction_text = self.small_font.render("Press ENTER to view leaderboard or ESC to quit", True, (200, 200, 200))

        self.score = score

        # Save to leaderboard if qualified
        if is_high_score(self.score):
            add_score(self.score)

        # 🎵 Play game over music
        pygame.mixer.music.stop()
        pygame.mixer.music.load("music/lose.wav")
        pygame.mixer.music.play()

    def draw(self):
        super().draw()
        w, h = self._screen.get_width(), self._screen.get_height()

        spacing = 50
        center_y = h // 2

        game_over_rect = self.game_over_text.get_rect(center=(w // 2, center_y - spacing))
        message_rect = self.message_text.get_rect(center=(w // 2, center_y))
        instruction_rect = self.instruction_text.get_rect(center=(w // 2, center_y + spacing))

        self._screen.blit(self.game_over_text, game_over_rect)
        self._screen.blit(self.message_text, message_rect)
        self._screen.blit(self.instruction_text, instruction_rect)

    def process_event(self, event):
        super().process_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self._next_scene = LeaderboardScene(self._screen)
                self._is_valid = False
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

