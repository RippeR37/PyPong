from Systems.Network.tcp.tcp_server import TCPServer
from Systems.Network.Messages.IndexAssignmentProc import IndexAssignmentProc
from Systems.Network.Messages.ServerReadyProc import ServerReadyProc
from Systems.Network.Messages.GamestateUpdateProc import GameState, GameStateUpdateProc
import threading
import json


class ServerListenThread(threading.Thread):
    def __init__(self, host="127.0.0.1", port=7664):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self._is_running = False
        self._server = TCPServer(host, port, 2)
        self.init_callbacks()
        self._buffers = []
        self._game_state = GameState()
        self._client_start_round = 1  # Second player starts first TODO: make sure this changes to whoever lost last

    def _reset_game_state(self):
        self._game_state = GameState()

    def _signal_start_if_ready(self):
        if len(self._server._clients) == 2:
            self._reset_game_state()
            self._server.send_all(ServerReadyProc().to_json())

    def _process_data(self, client, data):
        trimmed_data = data[1:-1]
        try:
            json_proc = json.loads(trimmed_data)

            if json_proc['proc'] == 'start_round':
                self._process_signal_start_round(client)
            elif json_proc['proc'] == 'game_state_update':
                self._process_game_state_update(client, json_proc)
        except:
            print("Wrong trimmed data: '{}'".format(trimmed_data))

    def _process_signal_start_round(self, client):
        if self._game_state.ball.vx == 0.0 and self._game_state.ball.vy == 0.0:
            client_index = self._server.get_client_index(client)
            if client_index == self._client_start_round:
                print("STARTING ROUND!")
                self._game_state.ball.vx = 0.33
                self._game_state.ball.vy = 0.66

    def _process_game_state_update(self, client, json_proc):
        gsup = GameStateUpdateProc(None).from_json(json_proc)
        ball = self._game_state.ball

        # Update ball position
        ball.x += ball.vx * 0.005
        ball.y += ball.vy * 0.005

        # Check if ball is in rect
        if ball.x < -1.0:
            ball.x = -1.0
            ball.vx = -ball.vx
        if ball.y < -1.0:
            ball.y = -1.0
            ball.vy = -ball.vy
        if ball.x > 1.0:
            ball.x = 1.0
            ball.vx = -ball.vx
        if ball.y > 1.0:
            ball.y = 1.0
            ball.vy = -ball.vy

        # Update ball's state in client's message and broadcast it along
        gsup.data['game_state'].ball = ball
        self._server.send_all_except(gsup.to_json(), client)

    def init_callbacks(self):
        # Index Assignment lambda
        self._server.index_assign_msg = lambda index: IndexAssignmentProc(index).to_json()

        # New client connected
        self._server.callbacks_connect.append(
            lambda client:
                print("New client ({}: {}) connected!".format(
                        self._server.get_client_index(client),
                        client.getpeername()
                    )
                )
        )
        self._server.callbacks_connect.append(
            lambda client:
                self._signal_start_if_ready()
        )

        # Server full
        self._server.callbacks_server_full.append(
            lambda client:
                print("Attempt to connect to full server from {}".format(client.getpeername()))
        )

        # Client lost connection
        self._server.callbacks_connection_lost.append(
            lambda client:
                print("Connection lost from client {}".format(client.getpeername()))
        )

        # Disconnected client
        self._server.callbacks_disconnect.append(
            lambda client:
                print("Client {} disconnected".format(client.getpeername()))
        )

        # Incoming data
        self._server.callbacks_incoming_data.append(
            lambda client, data:
                self._process_data(client, data)
        )

    def run(self):
        if not self._is_running:
            self._server.bind()
            self._server.listen()
            self._is_running = True

    def stop(self):
        self._server._listening = False
