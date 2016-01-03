from Systems.Engine.Scene import Scene
import pygame


class GameplayScene(Scene):
    def __init__(self):
        super().__init__(True, False)
        self._end = False
        self._window = None
        self._window_size = (600, 480)
        self._init_window()

    def _init_window(self):
        pygame.init()
        self._window = pygame.display.set_mode(self._window_size)
        self._swap_buffers()

    def _swap_buffers(self):
        pygame.display.flip()
        self._window.fill((0, 0, 0))  # black (RGB)

    def update(self, dt):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._end = True

    def render(self):
        if not self._end:
            # render here
            self._swap_buffers()

    def process_scene_stack(self, scene_stack, scene_index):
        if self._end:
            scene_stack.clear()  # TODO: implement better scene stack processing then quiting
