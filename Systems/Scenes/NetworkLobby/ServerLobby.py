from Systems.Engine.Scene import Scene
from Systems.Scenes.Gameplay.GameplayScene import GameplayScene


class ServerLobby(Scene):
    def __init__(self):
        super().__init__(True, False)
        self._gameplay_ready = True

    def update(self, dt):
        pass

    def render(self):
        print("You are in server lobby!")

    def process_scene_stack(self, scene_stack, scene_index):
        if self._gameplay_ready:
            scene_stack.push(GameplayScene())
