import pygame


class Window(object):
    def __init__(self, size, title, bg_color=(0,0,0)):
        self._window = None
        self._size = size
        self._title = title
        self._bg_color = bg_color

    def create(self):
        pygame.init()
        self._window = pygame.display.set_mode(self._size)
        self.set_title(self._title)
        self.swap()

    def swap(self):
        pygame.display.flip()
        self._window.fill(self._bg_color)

    def set_title(self, title):
        self._title = title
        pygame.display.set_caption(self._title)

    def get_title(self):
        return self._title

    def get_surface(self):
        return self._window

    def get_size(self):
        return self._size
