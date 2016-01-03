from Systems.Engine.Scene import Scene


class ClientLobby(Scene):
    def __init__(self):
        super().__init__(True, False)

    def update(self, dt):
        pass

    def render(self):
        print("You are in client lobby!")

    def process_scene_stack(self, scene_stack, scene_index):
        pass
