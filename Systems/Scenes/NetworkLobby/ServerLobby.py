from Systems.Engine.Scene import Scene
from Systems.Scenes.Gameplay.WaitingRoomScene import WaitingRoomScene
from Systems.Network.PyPongClient import PyPongClient
from Systems.Network.PyPongServerThread import PyPongServerThread


class ServerLobby(Scene):
    def __init__(self):
        super().__init__(True, False)
        self._connected = False
        self._host_ip = "localhost"
        self._host_port = 7664
        self._client = None
        self._server_listener = None
        self._start_server()

    def _start_server(self):
        print("[SERVER] Provide port on which you want to host your game or leave empty to use default")
        input_port = input("[SERVER] Port (7664): ")

        if len(input_port) > 0:
            self._host_port = int(input_port)

        print("[SERVER] Starting localhost server on port {}".format(self._host_port))
        self._server_listener = PyPongServerThread(self._host_ip, self._host_port)
        self._server_listener.start()
        print("[SERVER] Server started on {}:{}".format(self._host_ip, self._host_port))

    def _stop_server(self):
        print("[SERVER] Server is stopping...")
        self._server_listener.stop()
        self._server_listener.join()
        print("[SERVER] Server stopped!")

    def update(self, dt):
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
            scene_stack.push(WaitingRoomScene(self._client))
