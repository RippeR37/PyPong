
class Scene(object):
    def __init__(self, stackable=True, stack_usable=True):
        self._is_stackable = stackable
        self._is_stack_usable = stack_usable

    def is_stackable(self):
        return self._is_stackable

    def is_stack_usable(self):
        return self._is_stack_usable

    def update(self, dt):
        pass

    def render(self):
        pass

    def process_scene_stack(self, scene_stack, scene_index):
        pass
