import socket
import threading
import _functions as _f
import platform


class Server(threading.Thread):

    def __init__(self, conn, sock, addr, clients, DATA_FOLDER):
        threading.Thread.__init__(self)
        self.conn = conn
        self.sock = sock
        self.addr = addr
        self.clients = clients
        self.DATA_FOLDER = DATA_FOLDER

    def run(self):
        threads = []
        threads.append(self.name)
        self.conn.sendall("You have connected to the FTP server".encode())
        self.running = True
        self.username = self.conn.recv(8192).decode()
        print(f"Thread {threading.active_count() - 1} started. "
              f"Handling connection from user '{self.username}' "
              f"at connection {self.addr}")
        while self.running:

            try:
                data = self.conn.recv(1024).decode()
                if not data:
                    return
                elif data == "dc":
                    print(
                        f"User: {self.username} running on thread {threading.active_count() - 1} disconnected.\n"
                    )
                    self.clients.remove(self.conn)
                    break
                else:
                    returned = _f.apply_command(self.sock, self.conn, data,
                                                self.username,
                                                self.DATA_FOLDER, self.clients)
                    self.send_to_client(self.conn, returned)
            except OSError:
                print(
                    f"User: {self.username} running on thread {threading.active_count() - 1} disconnected.\n"
                )
                self.clients.remove(self.conn)
                break

    def send_to_client(self, conn, data):
        if type(data) == list:
            data_str = str(data)
            conn.send(data_str.encode())
        elif data is None:
            pass
        else:
            conn.send(data.encode())


def main():
    SERVER = '127.0.0.1'
    PORT = 44554
    operation_system = platform.platform()
    if "Windows" in operation_system:
        DATA_FOLDER = "Data\\"
        print("Server is running on a Windows system")
    elif "Linux" or "Mac" in operation_system:
        DATA_FOLDER = "Data/"
        print("Server is running on a Linux system")
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
            Server(conn, sock, addr, clients, DATA_FOLDER).start()


if __name__ == '__main__':
    main()
