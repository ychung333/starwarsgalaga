"""
A class to manage transitions from one scene to another.
"""

class SceneManager:
    """Manages scene switching and updates."""

    def __init__(self, screen):
        """Initialize with the display screen."""
        self._screen = screen
        self._scenes = []
        self._current_scene = None

    def push(self, scene):
        """Push a new scene onto the stack and start it."""
        if self._current_scene:
            self._current_scene.end_scene()
        self._current_scene = scene
        self._current_scene.start_scene()

    def handle_event(self, event):
        """Pass input events to the current scene."""
        if self._current_scene:
            self._current_scene.process_event(event)

    def update(self, delta_time):
        """Update the current scene and transition if it's no longer valid."""
        if self._current_scene:
            self._current_scene.update_scene()
            if not self._current_scene.is_valid():
                self._scenes.pop(0)
                if self._scenes:
                    self.push(self._scenes[0])
                else:
                    self._current_scene = None

    def render(self):
        """Render the current scene."""
        if self._current_scene:
            self._current_scene.draw()
            self._current_scene.render_updates()

    def add_scene(self, scene):
        """Queue a scene to be shown next."""
        self._scenes.append(scene)
        if self._current_scene is None:
            self.push(scene)

    def current_scene(self):
        return self._current_scene
