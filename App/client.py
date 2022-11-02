import threading
import socket


class Client(threading.Thread):

    def __init__(self, sock, stop, username):
        threading.Thread.__init__(self)
        self.sock = sock
        self.stop = stop
        self.username = username

    def run(self):
        print(self.sock.recv(1024).decode())
        print(f"Thread {self.name} started. Handeling connection")
        print(self.username)


def main():
    SERVER = '127.0.0.1'
    PORT = 44554
    stop = threading.Event()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        username = input("Please enter your username: ")
        sock.connect((SERVER, PORT))
        client = Client(sock, stop, username)
        client.start()
        client.join()


if __name__ == '__main__':
    main()
