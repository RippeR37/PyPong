import threading

from Systems.Network.tcp.tcp_server import TCPServer


class ServerListenThread(threading.Thread):
    def __init__(self, host="127.0.0.1", port=7664):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self._is_running = False
        self._server = TCPServer(host, port, 2)
        self.init_callbacks()

    def init_callbacks(self):
        # New client connected
        self._server.callbacks_connect.append(
            lambda client:
                print("New client ({}) connected!".format(client.getpeername()))
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
                print("Client {} sent data: {}".format(client.getpeername(), data.decode()))
        )
        self._server.callbacks_incoming_data.append(lambda client, data: client.send(data))

    def run(self):
        if not self._is_running:
            self._server.bind()
            self._server.listen()
            self._is_running = True

    def stop(self):
        self._server._listening = False
