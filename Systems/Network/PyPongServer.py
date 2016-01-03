from Systems.Network.ServerListenThread import ServerListenThread

class PyPongServer:
    def __init__(self, host="127.0.0.1", port=7664):
        self.host = host
        self.port = port
        self._server_listener = ServerListenThread(host, port)

    def stop_listener(self):
        self._server_listener.stop()
        self._server_listener.join()

    def start(self):
        print("Starting server...")
        self._server_listener.start()
        print("Server started on {}:{}".format(self.host, self.port))

        while True:
            cmd = input()
            if cmd == "quit":
                print("Server is stopping...")
                self.stop_listener()
                print("Server stopped!")
                break


if __name__ == "__main__":
    server = PyPongServer()
    server.start()
