from Systems.Engine.Scene import Scene


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
            pass  # TODO: implement this
