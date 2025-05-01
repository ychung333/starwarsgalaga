"""
Main game logic using the VideoGame base class.
"""

import pygame
from .scene_title import TitleScene
from .scene_gameplay import GamePlayScene
from .scenemanager import SceneManager
from .player import Player
from .enemy import Enemy
from .levels import generate_level
from .leaderboard import add_score, is_high_score
from . import assets

class GalagaGame:
    def __init__(self):
        pygame.init()
        self.window_width = 800
        self.window_height = 600
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Galaga Clone")
        self.clock = pygame.time.Clock()
        self.running = True

        self.scene_manager = SceneManager(self.screen)

        # Add title scene
        title_scene = TitleScene(self.screen)
        self.scene_manager.add_scene(title_scene)

    def run(self):
        while self.running:
            delta_time = self.clock.tick(60) / 1000.0  # Convert to seconds
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.scene_manager.handle_event(event)

            self.scene_manager.update(delta_time)

            # Transition to gameplay when title scene ends
            if self.scene_manager.current_scene() is None:
                gameplay_scene = GamePlayScene(self.screen)
                self.scene_manager.add_scene(gameplay_scene)

            self.scene_manager.render()
            pygame.display.flip()

        pygame.quit()



