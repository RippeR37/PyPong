from Systems.Network.TokenBuffer import TokenBuffer
from Systems.Network.tcp.tcp_client import TCPClient
from Systems.Network.Messages.GamestateUpdateProc import GameStateUpdateProc
from Systems.Network.Messages.StartRoundProc import StartRoundProc
import json


class PyPongClient:
    def __init__(self, host="localhost", port=7664):
        self._client = TCPClient(host, port)
        self._init_callbacks()
        self._buffer = TokenBuffer()
        self.proc_callback = lambda json_proc: None
        self.set_default_proc_callback()

    def _init_callbacks(self):
        self._client.callbacks_incoming_data.append(
            lambda sock, data:
                self.update_client(data)
        )

    def set_default_proc_callback(self):
        self.proc_callback = lambda json_proc: True  # don't consume message but wait for proper handler to consume it

    def bind_proc_callback(self, callback):
        self.proc_callback = callback

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

    def update_host_game_state(self, game_state):
        self._client.send(GameStateUpdateProc(game_state).to_json())

    def signal_round_start(self):
        self._client.send(StartRoundProc().to_json())

    def update_client(self, incoming_data):
        self._buffer.push(incoming_data)

        while True:
            current_proc = self._buffer.peek_first_token('$', '&')

            if len(current_proc) > 0:
                result = None
                try:
                    json_proc = json.loads(current_proc)
                    result = self.proc_callback(json_proc)
                except json.JSONDecodeError:
                    print("[CLIENT] Received invalid JSON procedure: '{}'".format(current_proc))
                except Exception as exc:
                    print("[CLIENT] Unhandled exception from JSON procedure callback: {}".format(exc))
                finally:
                    if result is None:
                        self._buffer.get_first_token('$', '&')  # consume this token as it's invalid or was used
                    elif not result:
                        self._buffer.get_first_token('$', '&')  # consume this token as it was used
                    else:
                        pass  # do not consume this token as it will be used in future
            else:
                break
