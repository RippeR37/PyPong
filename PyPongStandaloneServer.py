from Systems.Network.PyPongServerThread import PyPongServerThread
import sys


class PyPongStandaloneServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self._server_listener = PyPongServerThread(host, port)

    def start(self):
        print("Starting server on {}:{}".format(self.host, self.port))
        self._server_listener.start()
        print("Server started on {}:{}".format(self.host, self.port))
        print("Type 'quit' to stop server.")

        while True:
            cmd = input()
            if cmd == "quit":
                print("Server is stopping...")
                self.stop_listener()
                print("Server stopped!")
                break

    def stop_listener(self):
        self._server_listener.stop()
        self._server_listener.join()


def main():
    host = "localhost"  # default host = localhost
    port = 7664  # default port = 7664 ( = PONG in T9 dictionary ;))

    if len(sys.argv) == 2:
        host = sys.argv[0]
        port = sys.argv[1]

    server = PyPongStandaloneServer(host, port)
    server.start()


if __name__ == "__main__":
    main()
