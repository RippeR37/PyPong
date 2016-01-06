from Systems.Network.tcp.tcp_server import TCPServer
from Systems.Network.Messages.IndexAssignmentProc import IndexAssignmentProc
from Systems.Network.Messages.ServerReadyProc import ServerReadyProc
from Systems.Network.Messages.GamestateUpdateProc import GameStateUpdateProc
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

    def _signal_start_if_ready(self):
        if len(self._server._clients) == 2:
            ready_proc = ServerReadyProc()
            ready_proc_json = ready_proc.to_json()
            self._server.send_all(ready_proc_json)

    def _process_data(self, client, data):
        try:
            trimmed_data = data[1:-1]
            gsup = GameStateUpdateProc(None).from_json(json.loads(trimmed_data))
            ball = gsup.data['game_state'].ball

            # Update ball position
            ball.x = ball.x + ball.vx * 0.005
            ball.y = ball.y + ball.vy * 0.005

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

            self._server.send_all_except(gsup.to_json(), client)
        except:
            print("Wrong trimmed data: '{}'".format(trimmed_data))


    def init_callbacks(self):
        # Index Assignment lambda
        self._server.index_assign_msg = lambda index: IndexAssignmentProc(index).to_json()

        # New client connected
        self._server.callbacks_connect.append(
            lambda client:
                print("New client ({}: {}) connected!".format(self._server.get_client_index(client), client.getpeername()))
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
