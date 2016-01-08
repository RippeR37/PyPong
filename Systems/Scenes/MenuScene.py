from Systems.Engine.Scene import Scene
from Systems.Scenes.NetworkLobby.ServerLobby import ServerLobby
from Systems.Scenes.NetworkLobby.ClientLobby import ClientLobby
from Systems.Utils.Console import Console


class MenuScene(Scene):
    def __init__(self):
        super().__init__(True, False)  # can be on top of other scenes, but is not used under any scenes
        self._mode = ""
        self._welcome_message()

    @staticmethod
    def _welcome_message():
        Console.cls()
        print("PyPong v0.1")
        print("===========\n")

    def update(self, dt):
        print("\nChoose:")
        print("- 'host' to host game")
        print("- 'connect' to connect to server")
        print("- 'quit' to quit game")
        print("")  # empty line delimiter
        self._mode = input("> ")

    def render(self):
        self._welcome_message()
        if self._mode not in ["host", "connect", "quit"]:
            print("Unrecognized input: {}".format(self._mode))

    def process_scene_stack(self, scene_stack, scene_index):
        if self._mode == "host":
            scene_stack.push(ServerLobby())
            return True
        elif self._mode == "connect":
            scene_stack.push(ClientLobby())
        elif self._mode == "quit":
            scene_stack.clear()
