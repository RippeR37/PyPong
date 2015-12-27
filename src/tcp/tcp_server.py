import socket
import select


class TCPServer:
    def __init__(self, host, port, max_clients):
        self._host = host
        self._port = port
        self._clients = []
        self._max_clients = max_clients
        self._buffer_size = 1024
        self._listening = False
        self.callbacks_connect = []
        self.callbacks_server_full = []
        self.callbacks_incoming_data = []
        self.callbacks_disconnect = []
        self.callbacks_connection_lost = []
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def bind(self):
        self._socket.bind((self._host, self._port))

    def listen(self):
        self._socket.listen(self._max_clients)
        self._listening = True

        while self._listening:
            read_sockets = select.select([self._socket] + self._clients, [], [], 1)[0]  # take only readable sockets

            for sock in read_sockets:
                if sock == self._socket:
                    client_socket, client_addr = sock.accept()
                    if len(self._clients) < self._max_clients:
                        self._clients.append(client_socket)
                        for callback in self.callbacks_connect:
                            callback(client_socket)
                    else:
                        for callback in self.callbacks_server_full:
                            callback(client_socket)
                        client_socket.close()
                else:
                    try:
                        data = sock.recv(self._buffer_size)
                        if data:
                            for callback in self.callbacks_incoming_data:
                                callback(sock, data)
                        else:
                            for callback in self.callbacks_disconnect:
                                callback(sock)
                            sock.close()
                            self._clients.remove(sock)
                    except:
                        for callback in self.callbacks_connection_lost:
                            callback(sock)
                        sock.close()
                        self._clients.remove(sock)

        self.close()

    def close(self):
        self._listening = False

        for client_socket in self._clients:
            client_socket.close()

        self._socket.close()
