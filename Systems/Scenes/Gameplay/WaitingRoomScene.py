from Systems.Engine.Scene import Scene
from Systems.Engine.Window import Window
from Systems.Network.PyPongClient import PyPongClient
from Systems.Network.Messages.IndexAssignmentProc import IndexAssignmentProc
from Systems.Scenes.Gameplay.GameplayScene import GameplayScene
import threading
import pygame


class WaitingRoomScene(Scene):
    def __init__(self, client, stats):
        assert isinstance(client, PyPongClient), "Invalid object type - client must be of PyPongClient type!"

        super().__init__(True, False)
        self._client = client
        self._client_listener = None
        self._window = Window((600, 400), "PyPong - Waiting in clientReadyScene")
        self._is_gameplay_ready = False
        self._end = False
        self._listen_to_host()
        self._index_assigned = -1
        self._index_assigned_read = False
        self._window.create()
        self._stats = stats

    def set_index(self, index):
        self._index_assigned = index
        self._index_assigned_read = False
        self._is_gameplay_ready = False

    def _listen_to_host(self):
        self._client_listener = threading.Thread(target=self._client.listen, daemon=True)
        self._client_listener.start()

    def _process_json_proc(self, json_proc):
        proc_name = json_proc['proc']

        if proc_name == "index_assignment":
            proc = IndexAssignmentProc(-1).from_json(json_proc)
            self.set_index(proc.data['index'])
            return False  # consume message
        elif proc_name == "server_ready":
            self._is_gameplay_ready = True
            self._client.set_default_proc_callback()
            return False  # consume message
        elif proc_name == "game_state_update":
            if self._is_gameplay_ready:
                return True  # leave that message to read in GameplayScene
            else:
                print("[CLIENT] Warning: Received GAME_STATE_UPDATE signal before SERVER_READY signal.")
                return False  # don't leave that message as it might pile up fast
        else:
            print("[CLIENT] Unknown procedure: {}".format(proc_name))
            return False  # consume message as it might pile up fasts

    def update(self, dt):
        self._client.bind_proc_callback(self._process_json_proc)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._end = True

        if not self._index_assigned_read:
            if self._index_assigned is not None:
                self._window.set_title("PyPong (Player {}) - Waiting...".format(self._index_assigned + 1))

    def render(self):
        if not self._end:
            self._window.swap()

    def process_scene_stack(self, scene_stack, scene_index):
        if self._is_gameplay_ready:
            self._is_gameplay_ready = False
            scene_stack.push(
                GameplayScene(self._client, self._client_listener, self._window, self._index_assigned, self._stats)
            )
        elif self._end:
            scene_stack.clear()
