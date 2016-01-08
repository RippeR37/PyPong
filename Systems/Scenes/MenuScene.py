from Systems.Engine.Scene import Scene
from Systems.Scenes.NetworkLobby.ServerLobby import ServerLobby
from Systems.Scenes.NetworkLobby.ClientLobby import ClientLobby


class MenuScene(Scene):
    def __init__(self):
        super().__init__(True, False)  # can be on top of other scenes, but is not used under any scenes
        self._mode = ""

    def update(self, dt):
        print("PyPong v0.1")
        print("- 'host' to host game")
        print("- 'connect' to connect to server")
        print("- 'quit' to quit game")
        self._mode = input("> ")

    def render(self):
        if self._mode == "host":
            print("Hosting game...")
        elif self._mode == "connect":
            print("Connecting...")
        elif self._mode == "quit":
            print("Quiting...")
        else:
            print("Unrecognized input: {}".format(self._mode))

    def process_scene_stack(self, scene_stack, scene_index):
        if self._mode == "host":
            scene_stack.push(ServerLobby())
            return True
        elif self._mode == "connect":
            scene_stack.push(ClientLobby())
            return True
        elif self._mode == "quit":
            scene_stack.clear()
