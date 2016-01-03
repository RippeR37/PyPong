from Systems.Engine.Scene import Scene


class SceneStack(object):
    def __init__(self):
        self._stack = []

    def count(self):
        return len(self._stack)

    def get_scene(self, index):
        return self._stack[index]

    def push(self, scene):
        assert isinstance(scene, Scene), "Attempt to push object not inherited from Scene class."
        self._stack.append(scene)

    def pop(self, n=1):
        for i in range(n):
            if len(self._stack) > 0:
                self._stack.pop()

    def remove(self, scene):
        self._stack.remove(scene)

    def clear(self):
        self._stack.clear()

    def cut_from(self, scene):
        index = self._stack.index(scene)
        self._stack = self._stack[:index]

    def cut_after(self, scene):
        index = self._stack.index(scene) + 1
        self._stack = self._stack[:index]
