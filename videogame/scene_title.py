"""
Title scene for the Galaga-style game.
"""

import pygame
import sys
from .scene import Scene
from . import assets

class TitleScene(Scene):
    """Scene that displays the game title and instructions."""

    def __init__(self, screen):
        super().__init__(screen, (0, 0, 0), soundtrack=assets.get("title"))
        self.font = pygame.font.SysFont("arial", 48)
        self.small_font = pygame.font.SysFont("arial", 24)
        self.title_text = self.font.render("Galaga Clone", True, (255, 255, 255))
        self.instruction_text = self.small_font.render(
            "Press any key to start or press ESC to quit", True, (255, 255, 255)
        )

    def draw(self):
        super().draw()
        title_rect = self.title_text.get_rect(center=(self._screen.get_width() // 2, self._screen.get_height() // 3))
        instruction_rect = self.instruction_text.get_rect(center=(self._screen.get_width() // 2, self._screen.get_height() // 2))
        self._screen.blit(self.title_text, title_rect)
        self._screen.blit(self.instruction_text, instruction_rect)

    def process_event(self, event):
        super().process_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            else:
                self._is_valid = False

