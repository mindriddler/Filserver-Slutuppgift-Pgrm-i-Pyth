import socket
import threading
import _functions as _f
# im setting "# pragma: no cover" on all methods containing socket as i dont
# know how to test them


class Server(threading.Thread):

    def __init__(self, conn, sock, addr, clients, DATA_FOLDER):
        threading.Thread.__init__(self)
        self.conn = conn
        self.sock = sock
        self.addr = addr
        self.clients = clients
        self.DATA_FOLDER = DATA_FOLDER

    def run(self):  # pragma: no cover
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
                    _f.apply_command(
                        self.conn,
                        data,
                        self.username,
                        self.DATA_FOLDER,
                        self.clients,
                    )
            except OSError:
                print(
                    f"User: {self.username} running on thread {threading.active_count() - 1} disconnected.\n"
                )
                self.clients.remove(self.conn)
                break


def main():  # pragma: no cover
    SERVER = '127.0.0.1'
    PORT = 44554
    operation_system = input(
        "Is the server running on Windows, Linux or Mac?: ").lower()
    if operation_system == "windows":
        DATA_FOLDER = "Data\\"
    elif operation_system == "linux" or operation_system == "Mac":
        DATA_FOLDER = "Data/"
    else:
        print("Invalid input. Exiting...")
        exit()
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


if __name__ == '__main__':  # pragma: no cover
    main()
