from Systems.Network.tcp.tcp_client import TCPClient
from Systems.Game.GameState import GameState
from Systems.Game.PlayerState import PlayerState
import json
import sys

class PyPongClient:
    def __init__(self, host="localhost", port=7664):
        self._client = TCPClient(host,port)
        self._init_callbacks()
        self._gameplay = None
        self._buffer = ""

    def bind_gameplay(self, gameplay):
        self._gameplay = gameplay

    def _init_callbacks(self):
        # TODO: use incoming data (game_state in json) to update current game_state
        self._client._callbacks_incoming_data.append(
            lambda sock, data:
                self.update_client(data)
        )

    def is_connected(self):
        return self._client.is_connected()

    def is_listening(self):
        return self._client.is_listening()

    def connect(self):
        self._client.connect()

    def listen(self):
        self._client.listen()

    def close(self):
        self._client.close()

    def update_host(self, game_state_json):
        self._client.send("$" + game_state_json + "&")

    def update_client(self, game_state_json):
        self._buffer += game_state_json.decode("utf-8")

        right_trimmed = self._buffer[:self._buffer.rfind('&')]  # Find end of last full-packet
        left_trimmed = right_trimmed[right_trimmed.rfind('$')+1:]
        self._buffer = self._buffer[self._buffer.rfind('&')+1:]

        try:
            sgs = json.loads(left_trimmed)
            player_1 = sgs['player1']
            player_2 = sgs['player2']
            opponent = PlayerState(float(player_2['x']), float(player_1['y']), int(player_2['pts']))
            self._gameplay._game_state.player2 = opponent

        except BaseException as e:
            print ("Invalid JSON response: '{}'\n".format(left_trimmed))
