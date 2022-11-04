import socket
import threading
import os
import os.path
import math
import tqdm
# im setting "# pragma: no cover" on all methods containing socket as i dont
# know how to test them


class Server(threading.Thread):

    def __init__(
        self,
        conn,
        sock,
        addr,
        clients,
    ):
        threading.Thread.__init__(self)
        self.conn = conn
        self.sock = sock
        self.addr = addr
        self.clients = clients
        self.SEPARATOR = "<SEPARATOR>"
        self.BUFFER_SIZE = 4096

    def run(self):  # pragma: no cover
        threads = []
        threads.append(self.name)
        self.conn.sendall("You have connected to the FTP server".encode())
        self.running = True
        # threading.Thread(target=self.broadcast_new_file,
        #  args=(
        #      self.conn,
        #      self.clients,
        #  )).start()
        while self.running:
            try:
                data = self.conn.recv(self.BUFFER_SIZE).decode()
                if not data:
                    return
                elif "username" in data:
                    username = "".join(data.split(":")[1:])
                    print(
                        f"Thread {threading.active_count() - 1} started. "
                        f"Handling connection from user: {username} at connection {self.addr}"
                    )
                else:
                    self.apply_command(self.conn, data, username,
                                       self.SEPARATOR, self.BUFFER_SIZE)
            except OSError:
                print(
                    f"User:{username} running on {self.name} disconnected.\n")
                break

    def apply_command(self, conn, data, username, SEPARATOR,
                      BUFFER_SIZE):  # pragma: no cover
        if "/files" in data:
            print(f"\nRecieved command '/files' from{username}. "
                  "They want to know what files we have.")
            all_files = self.files_on_serv()
            print(f"\nThe files we have are the following: {all_files}")
            self.send_to_client(conn, all_files)
        elif data == "dc":
            conn.close()
        elif "rm" in data:
            file = "".join(data.split(" ")[1:])
            print(f"\nRecieved command 'rm' from{username}. "
                  f"They want to remove the file {file}.")
            removed = self.remove_file(file)
            self.send_to_client(conn, removed)
        elif data == "dwnl":
            pass
        elif "upld" in data:
            # threading.Thread(target=self.upload,
            #  args=(conn, data, SEPARATOR,
            #        BUFFER_SIZE)).start()
            self.upload(conn, data, SEPARATOR, BUFFER_SIZE)
        elif "/fs" in data:
            try:
                file = "".join(data.split(" ")[1:])
                print(f"\nRecieved command '/fs' from{username}. "
                      f"They want to know what the file size of '{file}' is.")
                file_size = f"File size of '{file}' is: {self.check_file_size(file)}"
                print(f"\n{file_size}")
                self.send_to_client(conn, file_size)
            except OSError:
                data = "!!!That file does not exist!!!"
                print(data)
                self.send_to_client(conn, data)

    def send_to_client(self, conn, data):  # pragma: no cover
        if type(data) == list:
            data_str = str(data)
            conn.send(data_str.encode())
        else:
            conn.send(data.encode())

    def check_file_size(self, file):
        # https://stackoverflow.com/questions/5194057/better-way-to-convert-file-sizes-in-python
        file_size = os.path.getsize(f"Data/{file}")
        if file_size == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB")
        i = int(math.floor(math.log(file_size, 1024)))
        p = math.pow(1024, i)
        s = round(file_size / p, 2)
        return "%s %s" % (s, size_name[i])

    def files_on_serv(self):
        files = [f for f in os.listdir("Data")]
        return files

    def remove_file(self, file):
        try:
            os.remove(f"Data/{file}")
            data = f"\nFile '{file}' has been removed."
            print(data)
            return data
        except OSError:
            data = f"\n!!!File '{file}' does not exist!!!"
            print(data)
            return data

    def upload(self, conn, data, SEPARATOR, BUFFER_SIZE):
        print("UL thread started")
        file_name, file_size = data.split(SEPARATOR)
        file_name = os.path.basename(file_name)
        file_size = int(file_size)
        progress = tqdm.tqdm(range(file_size),
                             f"Receiving {file_name}",
                             unit="B",
                             unit_scale=True,
                             unit_divisor=1024)
        with open(f"Data/{file_name}", "wb") as f:
            while True:
                bytes_read = conn.recv(BUFFER_SIZE)
                if not bytes_read:
                    break
                f.write(bytes_read)
                progress.update(len(bytes_read))
            f.close()
            threading.exit()

    def download(self, data):
        pass

    # def broadcast_new_file(self, conn, clients):
    #     print("thread started")
    #     file_list = [f for f in os.listdir("Data")]
    #     while True:
    #         files = os.listdir("Data")
    #         paths = [os.path.join("Data", basename) for basename in files]
    #         newest_file = max(paths, key=os.path.getctime)
    #         for conn in clients:
    #             conn.send(
    #                 f"New file has been added to the server: '{newest_file}'".
    #                 encode())


def main():  # pragma: no cover
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
