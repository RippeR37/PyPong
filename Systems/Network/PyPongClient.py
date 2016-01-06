from Systems.Network.tcp.tcp_client import TCPClient
import json
import sys


class PyPongClient:
    def __init__(self, host="localhost", port=7664):
        self._client = TCPClient(host,port)
        self._init_callbacks()
        self._buffer = ""
        self.proc_callback = lambda json_proc: None

    def _init_callbacks(self):
        # TODO: use incoming data (game_state in json) to update current game_state
        self._client._callbacks_incoming_data.append(
            lambda sock, data:
                self.update_client(data)
        )

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

    def update_host(self, game_state_json):
        self._client.send("$" + game_state_json + "&")

    def update_client(self, incoming_data):
        self._buffer += incoming_data

        while True:
            index_l = self._buffer.find('$')       # Find start of first full-proc
            if index_l == -1:
                break
            first_proc_1 = self._buffer[index_l+1:]
            index_r = first_proc_1.find('&')       # Find end of first full-proc
            first_proc_2 = first_proc_1[:index_r]

            if len(first_proc_2) > 0:
                self._buffer = first_proc_1[index_r+1:]
                try:
                    proc_json = json.loads(first_proc_2)
                    self.proc_callback(proc_json)
                except:
                    print("Invalid JSON procedure: '{}'".format(first_proc_2))
            else:
                break
