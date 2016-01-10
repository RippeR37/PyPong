from Systems.Engine.Scene import Scene
from Systems.Game.PlayerStats import PlayerStats
from Systems.Scenes.NetworkLobby.ServerLobby import ServerLobby
from Systems.Scenes.NetworkLobby.ClientLobby import ClientLobby
from Systems.Utils.Console import Console


class MenuScene(Scene):
    def __init__(self):
        super().__init__(True, False)  # can be on top of other scenes, but is not used under any scenes
        self._mode = ""
        self._stats = None

    def _welcome_message(self):
        Console.cls()
        print("PyPong v0.1")
        print("===========\n\n")

        if self._stats is not None:
            print("Welcome {} (wins: {}, loses: {})".format(
                self._stats.name,
                self._stats.get_wins(),
                self._stats.get_loses()
            ))

    def update(self, dt):
        self._welcome_message()

        print("Choose:")
        print("- 'host' to host game")
        print("- 'connect' to connect to server")
        print("- 'login' to login as player")
        print("- 'quit' to quit game")
        print("")  # empty line delimiter

        self._mode = input("> ")
        if self._mode == "login":
            login = input("Your nick: ")
            self._stats = PlayerStats(login)
            self._stats.load()

    def render(self):
        self._welcome_message()

        if self._mode not in ["host", "connect", "quit", "login"]:
            print("Unrecognized input: {}".format(self._mode))

    def process_scene_stack(self, scene_stack, scene_index):
        if self._mode == "host":
            scene_stack.push(ServerLobby(self._stats))
            return True
        elif self._mode == "connect":
            scene_stack.push(ClientLobby(self._stats))
        elif self._mode == "quit":
            scene_stack.clear()
