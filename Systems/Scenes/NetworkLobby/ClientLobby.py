from Systems.Engine.Scene import Scene
from Systems.Scenes.Gameplay.WaitingRoomScene import WaitingRoomScene
from Systems.Network.PyPongClient import PyPongClient


class ClientLobby(Scene):
    def __init__(self):
        super().__init__(True, False)
        self._connected = False
        self._host_ip = "localhost"
        self._host_port = 7664
        self._client = None

    def update(self, dt):
        input_ip = input("IP: ")
        input_port = input("Port: ")

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
            print("Connected to server, entering game room.")
        else:
            print("Could not connect to server!")

    def process_scene_stack(self, scene_stack, scene_index):
        if self._connected:
            scene_stack.push(WaitingRoomScene(self._client))
