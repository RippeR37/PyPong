import threading


class ClientListenThread(threading.Thread):
    def __init__(self, client):
        self.client = client
        threading.Thread.__init__(self);

    def run(self):
        print("Starting listening...")
        self.client.listen()
        print("Disconnected.")

    def stop(self):
        self.client.close()