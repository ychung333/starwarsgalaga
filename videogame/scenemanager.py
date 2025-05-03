"""
Scene Manager for transitioning between scenes.
"""

class SceneManager:
    def __init__(self, screen):
        self._screen = screen
        self._current_scene = None

    def add_scene(self, scene):
        """Add a new scene and start it."""
        if self._current_scene:
            self._current_scene.end_scene()
        self._current_scene = scene
        self._current_scene.start_scene()

    def update(self, delta_time):
        """Update the current scene and handle transitions."""
        if self._current_scene:
            self._current_scene.update_scene()
            if not self._current_scene.is_valid():
                next_scene = getattr(self._current_scene, "_next_scene", None)
                if next_scene:
                    self._current_scene.end_scene()
                    self._current_scene = next_scene
                    self._current_scene.start_scene()
                else:
                    self._current_scene.end_scene()
                    self._current_scene = None

    def render(self):
        """Draw the current scene."""
        if self._current_scene:
            self._current_scene.draw()

    def handle_event(self, event):
        """Pass events to the current scene."""
        if self._current_scene:
            self._current_scene.process_event(event)

    def current_scene(self):
        """Return the current scene."""
        return self._current_scene

