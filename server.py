import socket
import threading
import time
import _functions as _f
import platform
from _datahandler import DataHandler


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
                    # yapf: disable
                    returned = _f.apply_command(self.conn, data,
                                                self.username,
                                                self.DATA_FOLDER,
                                                self.clients)
                    self.send_to_client(self.conn, self.clients, returned)
                    # yapf: enable
            except OSError:
                print(
                    f"User: {self.username} running on thread {threading.active_count() - 1} disconnected.\n"
                )
                self.clients.remove(self.conn)
                break

    def apply_command(conn, data, username, DATA_FOLDER):
        if data == "files":
            print(f"\nRecieved command 'files' from: {username}.")
            conn.sendall("files".encode())
            all_files = _f.files_on_serv()
            return all_files

        elif data == "dc":
            conn.close()

        elif data == "remove":
            file = conn.recv(1024).decode()
            conn.sendall("remove".encode())
            print(f"\nRecieved command 'remove' from user: {username}.")
            removed = _f.remove_file(file, DATA_FOLDER)
            return removed

        elif data == "download":
            print(f"\nRecieved command 'download' from user: {username}.")
            DataHandler().upload_to_client(conn, DATA_FOLDER)

        elif data == "upload":
            conn.sendall("upload".encode())
            print(f"\nRecieved command 'upload' from user: {username}.")
            return DataHandler().server_recieve(conn, username, DATA_FOLDER)

        elif data == "file_size":
            try:
                file = conn.recv(1024).decode()
                conn.sendall("file_size".encode())
                print(f"\nRecieved command 'file_size' from user: {username}.")
                file_size = (
                    f"File size of '{file}' is: {_f.check_file_size(file, DATA_FOLDER)}"
                )
                return file_size
            except OSError:
                data = "!!!That file does not exist!!!"
                print(data)
                return data

    def send_to_client(self, conn, clients, data):
        if type(data) == list:
            data_str = str(data)
            conn.send(data_str.encode())
        elif "uploaded" in data:
            for conn in clients:
                conn.send("broadcast".encode())
                time.sleep(1)
                conn.send(data.encode())
        elif data is None:
            pass
        else:
            conn.send(data.encode())


def main():
    SERVER = "127.0.0.1"
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


if __name__ == "__main__":
    main()
