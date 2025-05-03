"""
Scene that displays the top 3 high scores.
"""

import pygame
import sys
from .scene import Scene
from .scene_title import TitleScene
from .leaderboard import load_scores

class LeaderboardScene(Scene):
    def __init__(self, screen):
        super().__init__(screen, (0, 0, 0))
        self.font = pygame.font.SysFont("arial", 36)
        self.small_font = pygame.font.SysFont("arial", 24)
        self.title = self.font.render("Leaderboard - Top 3 Scores", True, (255, 255, 255))
        self.scores = load_scores()
        self.score_texts = [
            self.small_font.render(f"{i+1}. {name} - {score}", True, (255, 255, 255))
            for i, (name, score) in enumerate(self.scores)
        ]
        self.instruction = self.small_font.render("Press ENTER to return to Title or ESC to quit", True, (255, 255, 255))

    def draw(self):
        super().draw()
        screen_center_x = self._screen.get_width() // 2
        y = 100
        self._screen.blit(self.title, self.title.get_rect(center=(screen_center_x, y)))

        for i, text_surface in enumerate(self.score_texts):
            y += 50
            self._screen.blit(text_surface, text_surface.get_rect(center=(screen_center_x, y)))

        y += 50
        self._screen.blit(self.instruction, self.instruction.get_rect(center=(screen_center_x, y)))

    def process_event(self, event):
        super().process_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self._next_scene = TitleScene(self._screen)
                self._is_valid = False
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

