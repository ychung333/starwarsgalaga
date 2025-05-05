"""Scene objects for making games with PyGame."""

import pygame

class Scene:
    """Base class for making PyGame Scenes."""

    def __init__(self, screen, background_color, screen_flags=None, soundtrack=None):
        self._screen = screen
        if not screen_flags:
            screen_flags = pygame.SCALED
        self._background = pygame.Surface(self._screen.get_size(), flags=screen_flags)
        self._background.fill(background_color)
        self._frame_rate = 60
        self._is_valid = True
        self._soundtrack = soundtrack  # store the path for this scene's music
        self._render_updates = None

    def draw(self):
        self._screen.blit(self._background, (0, 0))

    def process_event(self, event):
        if event.type == pygame.QUIT:
            self._is_valid = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._is_valid = False

    def is_valid(self):
        return self._is_valid

    def update_scene(self):
        pass

    def render_updates(self):
        pass

    def start_scene(self):
        if self._soundtrack:
            try:
                pygame.mixer.music.load(self._soundtrack)
                pygame.mixer.music.set_volume(0.1)
                pygame.mixer.music.play(loops=-1)
            except pygame.error as e:
                print(f"Music error: {e}")
                pygame.mixer.music.stop()

    def end_scene(self):
        if self._soundtrack and pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

    def frame_rate(self):
        return self._frame_rate

