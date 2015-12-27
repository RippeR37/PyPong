from src.tcp.tcp_client import TCPClient
from src.ClientListenThread import ClientListenThread


client = TCPClient("localhost", 7664)
clientListener = ClientListenThread(client)
client.connect()
clientListener.start()

while True:
    msg = input("Send message ('q' to quit): ")

    if msg == "q":
        clientListener.stop()
        clientListener.join()
        break

    if client.is_connected():
        client.send(msg)
    else:
        break

print("Should end now")
