from Systems.Network.tcp.tcp_server import TCPServer
from Systems.Network.Messages.IndexAssignmentProc import IndexAssignmentProc
from Systems.Network.Messages.ServerReadyProc import ServerReadyProc
from Systems.Network.Messages.GamestateUpdateProc import GameState, GameStateUpdateProc
from Systems.Network.TokenBuffer import TokenBuffer
import threading
import json


class PyPongServerThread(threading.Thread):
    def __init__(self, host="127.0.0.1", port=7664):
        threading.Thread.__init__(self, daemon=True)
        self.host = host
        self.port = port
        self._is_running = False
        self._server = TCPServer(host, port, 2)
        self.init_callbacks()
        self._buffers = dict()
        self._game_state = GameState()
        self._client_start_round = 1  # Second player starts first

    def _add_buffer(self, client):
        # print("Creating buffer for client: {}".format(client.getpeername()))
        self._buffers[client.getpeername()] = TokenBuffer()
        return None

    def _remove_buffer(self, client):
        # print("Removing buffer of client: {}".format(client.getpeername()))
        del self._buffers[client.getpeername()]
        return None

    def init_callbacks(self):
        # Index Assignment lambda
        self._server.index_assign_msg = lambda index: IndexAssignmentProc(index).to_json()

        # New client connected
        self._server.callbacks_connect.append(lambda client: self._add_buffer(client))
        self._server.callbacks_connect.append(
            lambda client:
                print("[SERVER] New client ({}, {}) connected.".format(
                    self._server.get_client_index(client),
                    client.getpeername())
                )
        )
        self._server.callbacks_connect.append(lambda client: self._signal_start_if_ready())

        # Server full
        self._server.callbacks_server_full.append(
            lambda client: print("[SERVER] Attempt to connect to full server from {}".format(client.getpeername()))
        )

        # Client lost connection
        self._server.callbacks_connection_lost.append(
            lambda client:
                print("[SERVER] Connection lost from client {}".format(client.getpeername()))
        )
        self._server.callbacks_connection_lost.append(lambda client: self._remove_buffer(client))

        # Disconnected client
        self._server.callbacks_disconnect.append(
            lambda client:
                print("[SERVER] Client {} disconnected".format(client.getpeername()))
        )
        self._server.callbacks_disconnect.append(lambda client: self._remove_buffer(client))

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

    def _reset_game_state(self):
        self._game_state = GameState()
        self._client_start_round = 1

    def _signal_start_if_ready(self):
        if len(self._server.clients) == 2:
            self._reset_game_state()
            self._server.send_all(ServerReadyProc().to_json())

    def _process_data(self, client, data):
        client_buffer = self._buffers.get(client.getpeername())
        client_buffer.push(data)

        while True:
            current_proc = client_buffer.get_first_token('$', '&')

            if len(current_proc) > 0:
                try:
                    json_proc = json.loads(current_proc)
                    if json_proc['proc'] == 'start_round':
                        self._process_signal_start_round(client)
                    elif json_proc['proc'] == 'game_state_update':
                        self._process_game_state_update(client, json_proc)
                except json.JSONDecodeError:
                    print("[SERVER] Invalid JSON procedure: '{}'".format(current_proc))
                except Exception as exc:
                    print("[SERVER] Unhandled exception while parsing JSON procedure: {}".format(exc))
            else:
                break

    def _process_signal_start_round(self, client):
        if self._game_state.ball.vx == 0.0 and self._game_state.ball.vy == 0.0:
            client_index = self._server.get_client_index(client)
            if client_index == self._client_start_round:
                self._game_state.ball.vx = 0.33
                self._game_state.ball.vy = 0.66

    def _process_game_state_update(self, client, json_proc):
        gsup = GameStateUpdateProc(None).from_json(json_proc)
        ball = self._game_state.ball
        p1 = gsup.data['game_state'].player1
        p2 = gsup.data['game_state'].player2

        # Update ball position
        ball.x += ball.vx * 0.01
        ball.y += ball.vy * 0.01

        # Check collision with paddles
        p1_rect = self.get_player_rect(p1)
        p2_rect = self.get_player_rect(p2)
        b_rect = self.get_ball_rect(ball)

        if self.intersect(p1_rect, b_rect):
            ball.x = (p1_rect[0] + p1_rect[2]) * 2.0 - 1.0
            ball.vx = abs(ball.vx)
        elif self.intersect(p2_rect, b_rect):
            ball.x = p2_rect[0] - b_rect[2]
            ball.vx = -1.0 * abs(ball.vx)

        # Check if ball doesn't touch upper or lower edge and has to bounce
        if ball.y < -1.0:
            ball.y = -1.0
            ball.vy = -ball.vy
        if ball.y > 1.0:
            ball.y = 1.0
            ball.vy = -ball.vy

        # Check if ball didn't escape from game area (leading to end of round)
        if ball.x < -1.0:
            ball.reset()
            self._game_state.player2.pts += 1
            self._client_start_round = 0
        if ball.x > 1.0:
            ball.reset()
            self._game_state.player1.pts += 1
            self._client_start_round = 1

        # Update ball's state in client's message and broadcast it along
        gsup.data['game_state'].ball = ball
        gsup.data['game_state'].player1.pts = self._game_state.player1.pts
        gsup.data['game_state'].player2.pts = self._game_state.player2.pts
        self._server.send_all_except(gsup.to_json(), client)

    @staticmethod
    def intersect(r1, r2):
        return \
            (r1[0] < r2[0] + r2[2]) and (r1[0] + r1[2] > r2[0]) and \
            (r1[1] < r2[1] + r2[3]) and (r1[1] + r1[3] > r2[1])

    @staticmethod
    def get_player_rect(player_data):
        width = 1.0 / 30.0
        height = 1.0 / 5.0

        pos_x = (player_data.x + 1.0) * 0.5 * (1.0 - width)
        pos_y = (player_data.y + 1.0) * 0.5 * (1.0 - height)

        return pos_x, pos_y, width, height

    @staticmethod
    def get_ball_rect(ball_data):
        width = 1.0 / 30.0
        height = 1.0 / 20.0

        pos_x = (ball_data.x + 1.0) * 0.5 * (1.0 - width)
        pos_y = (ball_data.y + 1.0) * 0.5 * (1.0 - height)

        return pos_x, pos_y, width, height
