import socket
from time import sleep

class SocketHandler:
    def __init__(self, host, port):
        self.host = host
        self.port = port


    def send(self, data):
        sock = socket.socket()

        try:
            sock.connect((self.host, self.port))
        except Exception as ex:
            print("cannot connect to the socket, exception: {}".format(ex))

        for i in data:
            sock.send(str(i).encode())
        sock.close()




if __name__ == "__main__":
    sock_obj = SocketHandler("127.0.0.1", 8010)
    sock_obj.send(range(1000))

