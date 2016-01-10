from Systems.Engine.Scene import Scene
from Systems.Scenes.Gameplay.WaitingRoomScene import WaitingRoomScene
from Systems.Network.PyPongClient import PyPongClient


class ClientLobby(Scene):
    def __init__(self, stats):
        super().__init__(True, False)
        self._connected = False
        self._host_ip = "localhost"
        self._host_port = 7664
        self._client = None
        self._stats = stats

    def update(self, dt):
        print("[CLIENT] Provide ip address and port of the server you want to connect to or leave empty to use default")
        input_ip = input("[CLIENT] IP (localhost): ")
        input_port = input("[CLIENT] Port (7664): ")

        if len(input_ip) > 0:
            self._host_ip = input_ip
        if len(input_port) > 0:
            self._host_port = int(input_port)

        # try to connect here
        self._client = PyPongClient(self._host_ip, self._host_port)
        self._client.connect()

        # if connected, go to gameplay
        if self._client.is_connected():
            self._connected = True

    def render(self):
        if self._connected:
            print("[CLIENT] Connected to server, entering game room.")
        else:
            print("[CLIENT] Could not connect to server!")

    def process_scene_stack(self, scene_stack, scene_index):
        if self._connected:
            scene_stack.push(WaitingRoomScene(self._client, self._stats))
