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
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.index_assign_msg = lambda index: str(index)

    def bind(self):
        self._socket.bind((self._host, self._port))

    @staticmethod
    def send_to(client, data):
        prefix = "$"
        sufix = "&"
        presufixed_data = prefix + data + sufix
        client.send(presufixed_data.encode())

    def send_all(self, data):
        for client in self._clients:
            self.send_to(client, data)

    def send_all_except(self, data, ignored_client):
        for client in self._clients:
            if client != ignored_client:
                self.send_to(client, data)

    def listen(self):
        self._socket.listen(self._max_clients)
        self._listening = True

        while self._listening:
            read_sockets = select.select([self._socket] + self._clients, [], [], 1)[0]  # take only readable sockets

            for sock in read_sockets:
                if sock == self._socket:                                # Operation on server's socket
                    client_socket, client_addr = sock.accept()
                    if len(self._clients) < self._max_clients:              # New valid client
                        self._clients.append(client_socket)
                        self.assign_client_index(client_socket)
                        for callback in self.callbacks_connect:
                            callback(client_socket)
                    else:                                                   # Server-full client
                        for callback in self.callbacks_server_full:
                            callback(client_socket)
                        client_socket.close()
                else:                                                   # Operation on client's socket
                    try:
                        data = sock.recv(self._buffer_size)
                        if data:                                            # New valid incoming data
                            for callback in self.callbacks_incoming_data:
                                callback(sock, data.decode())
                        else:                                               # Client disconnects
                            for callback in self.callbacks_disconnect:
                                callback(sock)
                            sock.close()
                            self._clients.remove(sock)
                            self.assign_all_indexes()
                    except:                                                 # Client loses connection
                        for callback in self.callbacks_connection_lost:
                            callback(sock)
                        sock.close()
                        self._clients.remove(sock)
                        self.assign_all_indexes()

        self.close()

    def close(self):
        self._listening = False

        for client_socket in self._clients:
            client_socket.close()

        self._socket.close()

    def get_client_index(self, client):
        return self._clients.index(client)

    def assign_client_index(self, client):
        if self.index_assign_msg:
            index = self.get_client_index(client)
            self.send_to(client, self.index_assign_msg(index))

    def assign_all_indexes(self):
        for client in self._clients:
            self.assign_client_index(client)
