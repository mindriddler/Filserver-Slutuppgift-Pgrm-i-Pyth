import socket
import threading


class Server(threading.Thread):

    def __init__(self, conn, sock, addr, clients):
        threading.Thread.__init__(self)
        self.conn = conn
        self.sock = sock
        self.addr = addr
        self.clients = clients

    def run(self):
        print(f"Thread {threading.active_count() - 1} started. Handling "
              "connection from {self.addr}")
        self.conn.sendall("You have connected to the FTP server".encode())
        self.running = True
        while self.running:
            print("test")
            break


def main():
    SERVER = '127.0.0.1'
    PORT = 44554
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((SERVER, PORT))
        print("Socket bound to port %s" % (PORT))
        sock.listen(5)
        print("Listening for connections.")
        clients = []
        while True:
            conn, addr = sock.accept()
            clients.append(conn)
            print("Got connection from", addr)
            Server(conn, sock, addr, clients).start()


if __name__ == '__main__':  # pragma: no cover
    main()