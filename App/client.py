import threading
import socket
import time
import os
import tqdm


class Client(threading.Thread):

    def __init__(self, sock, stop, username, threads):
        threading.Thread.__init__(self)
        self.sock = sock
        self.stop = stop
        self.username = username
        self.threads = threads
        self.SEPARATOR = "<SEPARATOR>"
        self.BUFFER_SIZE = 4096

    def run(self):
        self.sock.sendall(self.username.encode())
        print(self.sock.recv(8192).decode())
        self.threads.append(
            f"{self.name}:{socket.gethostbyname(socket.gethostname())}")
        threading.Thread(target=self.menu,
                         args=(self.sock, self.stop, self.threads,
                               self.username, self.BUFFER_SIZE,
                               self.SEPARATOR)).start()
        while not self.stop.is_set():
            self.recieve_data(self.sock, self.stop)

    def menu(self, sock, stop, threads, username, BUFFER_SIZE, SEPARATOR):
        threads.append(self.name)
        while not stop.is_set():
            try:
                time.sleep(0.01)
                command = input(f"\n{username}\n"
                                "\n   COMMAND       | DESCRIPTION\n\n"
                                "rm   <FILE_NAME> | Removes a file\n"
                                "dwnl <FILE_NAME> | Upload a file\n"
                                "upld <FILE_PATH> | Download a file\n"
                                "/fs  <FILE_NAME> | Check file size\n"
                                "/files           | Check available files\n\n"
                                "dc               | Disconnect\n\n")
                if command == "":
                    input(
                        "You didnt enter a command.\nTry again.\nPress any key to continue."
                    )
                    os.system('clear')
                elif command == "dc":
                    sock.sendall(command.encode())
                    sock.close()
                    stop.set()
                    threads.remove(self.name)
                    break
                elif "upld" in command:
                    ul_thread = threading.Thread(target=self.upload,
                                                 args=(
                                                     sock,
                                                     command,
                                                     SEPARATOR,
                                                     BUFFER_SIZE,
                                                 ))
                    ul_thread.start()
                else:
                    sock.sendall(command.encode())
            except OSError as e:
                print(e)

    def recieve_data(self, sock, stop):
        data = sock.recv(8192).decode()
        if not data:
            sock.close()
            stop.set()
            return stop.set()
        elif "added to the server" in data:
            print(data)
            print("Write your menu command below!")
        else:
            print(data)
        # input("Press any key to continue to main menu")

    def upload(self, sock, command, SEPARATOR, BUFFER_SIZE):
        file_path = "".join(command.split(" ")[1:])
        file_name = "".join(file_path.split("/")[2:])
        file_size = os.path.getsize(file_path)
        sock.sendall(f"{command}{SEPARATOR}{file_size}".encode())
        progress = tqdm.tqdm(range(file_size),
                             f"Sending {file_name}",
                             unit_scale=True,
                             unit="B",
                             unit_divisor=1024)
        with open(file_path, "rb") as f:
            while True:
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    break
                sock.sendall(bytes_read)
                progress.update(len(bytes_read))


def main():  # pragma: no cover
    SERVER = '127.0.0.1'
    PORT = 44554
    stop = threading.Event()
    threads = []
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        print("Connecting to server.\nPlease standby.")
        time.sleep(3)  # Just for fun
        try:
            sock.connect((SERVER, PORT))
        except ConnectionRefusedError as e:
            input(f"{e}. Is the server running?\n\n"
                  "Press any key to continue.")
            return
        username = "username: " + input(f"\n\nConnect to {SERVER}:{PORT}\n"
                                        "Enter your username: ")
        client = Client(sock, stop, username, threads)
        client.start()
        client.join()


if __name__ == '__main__':
    main()
