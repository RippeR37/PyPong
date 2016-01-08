import socket
import select
import sys


class TCPClient:
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._buffer_size = 1024
        self._is_connected = False
        self._is_listening = False
        self.callbacks_incoming_data = []
        self.callbacks_disconnect = []
        self.callbacks_connection_lost = []
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def is_connected(self):
        return self._is_connected

    def is_listening(self):
        return self._is_listening

    def connect(self):
        if not self._is_connected:
            try:
                self._socket.connect((self._host, self._port))
                self._is_connected = True
            except ConnectionRefusedError:
                print("Could not connect to {}:{}".format(self._host, self._port))
                sys.exit(1)

    def send(self, data):
        if self._is_connected:
            prefix = "$"
            sufix = "&"
            prefix_data_sufix = prefix + data + sufix
            self._socket.send(prefix_data_sufix.encode())

    def read(self):
        if self._is_connected:
            return self._socket.recv(self._buffer_size).decode()  # blocking
        else:
            return None

    def listen(self):
        self._is_listening = True

        while self._is_listening and self._is_connected:
            read_sockets = select.select([self._socket], [], [], 1)[0]

            for sock in read_sockets:
                try:
                    data = sock.recv(self._buffer_size)
                    if data:
                        for callback in self.callbacks_incoming_data:
                            callback(sock, data.decode())
                    else:
                        for callback in self.callbacks_disconnect:
                            callback(sock)
                        self.close()
                        break
                except:
                    for callback in self.callbacks_disconnect:
                        callback(sock)
                    self.close()
                    break

        self.close()

    def close(self):
        self._socket.close()
        self._is_connected = False
        self._is_listening = False
