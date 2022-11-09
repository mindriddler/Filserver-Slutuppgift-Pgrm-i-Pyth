import socket
import threading
import _functions
from _datahandler import DataHandler_Server


class Server(threading.Thread):

    def __init__(self, conn, sock, addr, clients, DATA_FOLDER):
        threading.Thread.__init__(self)
        self.conn = conn
        self.sock = sock
        self.addr = addr
        self.clients = clients
        self.DATA_FOLDER = DATA_FOLDER

    def run(self):
        self.conn.sendall("You have connected to the FTP server".encode())
        self.running = True
        self.username = self.conn.recv(1024).decode()
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
                    self.conn.send("dc".encode())
                    self.conn.close()
                    break
                else:
                    returned = DataHandler_Server().apply_command_server(
                        self.sock,
                        self.conn,
                        data,
                        self.username,
                        self.DATA_FOLDER,
                    )
                    if returned is False:
                        self.running = False
                    else:
                        DataHandler_Server().send_data_to_client(
                            self.conn,
                            self.clients,
                            returned,
                        )
            except OSError:
                print(
                    f"User: {self.username} running on thread {threading.active_count() - 1} disconnected.\n"
                )
                try:
                    self.clients.remove(self.conn)
                    break
                except ValueError:
                    break


def main():
    SERVER = "127.0.0.1"
    PORT = 44554
    operation_system = _functions.check_os()
    if operation_system == "Windows":
        DATA_FOLDER = "Data\\"
        print("Windows detected. Setting data folder to 'Data\\'")
    else:
        DATA_FOLDER = "Data/"
        print("UNIX detected. Setting data folder to 'Data/'")
    try:
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
    except OSError:
        pass


if __name__ == "__main__":
    main()
