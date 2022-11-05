import threading
import socket
import os
from time import sleep
from _datahandler import DataHandler


class Client(threading.Thread):

    def __init__(self, sock, stop, username):
        threading.Thread.__init__(self)
        self.sock = sock
        self.stop = stop
        self.username = username

    def run(self):
        self.sock.sendall(self.username.encode())
        print(self.sock.recv(1024).decode())
        threading.Thread(target=self.menu,
                         args=(self.sock, self.stop, self.username)).start()
        # self.menu(self.sock, self.stop, self.username)
        while not self.stop.is_set():
            data = self.sock.recv(1024).decode()
            if not data:
                break
            else:
                self.recieve_data(self.sock, self.stop, data)

    def menu(self, sock, stop, username):
        while not stop.is_set():
            try:
                sleep(0.05)
                input("Press any key to continue")
                command = input(f"\nUsername: {username}\n"
                                "\nCOMMAND   | DESCRIPTION\n"
                                "---------------------------\n"
                                "remove    | Removes a file\n"
                                "download  | Upload a file\n"
                                "upload    | Download a file\n"
                                "file_size | Check file size\n"
                                "files     | Check available files\n"
                                "dc        | Disconnect\n\n"
                                "Enter command: ")
                if command == "":
                    input(
                        "You didnt enter a command.\nTry again.\nPress any key to continue."
                    )
                    os.system('clear')
                elif command == "dc":
                    sock.sendall(command.encode())
                    sock.close()
                    stop.set()
                    break
                elif command == "upload":
                    DataHandler().upload(sock, command)
                elif command == "file_size" or command == "remove":
                    sock.sendall(command.encode())
                    filename = input("Enter filename: ")
                    sock.sendall(filename.encode())
                elif command == "download":
                    sock.sendall(command.encode())
                else:
                    sock.sendall(command.encode())
            except OSError as e:
                print(e)

    def recieve_data(self, sock, stop, data):
        try:
            if not data:
                return
            if data == "download":
                DataHandler().client_recieve(sock)
            elif data == "files":
                data = sock.recv(1024).decode()
                print(data)
            elif data == "broadcast":
                data = sock.recv(1024).decode()
                print(data)
        except UnicodeDecodeError:
            DataHandler().client_recieve(sock)


def main():  # pragma: no cover
    SERVER = '127.0.0.1'
    PORT = 44554
    stop = threading.Event()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        print("Connecting to server.\nPlease standby.")
        # time.sleep(3)  # Just for fun
        try:
            sock.connect((SERVER, PORT))
        except ConnectionRefusedError as e:
            input(f"{e}. Is the server running?\n\n"
                  "Press any key to continue.")
            return
        username = input(f"\n\nConnect to {SERVER}:{PORT}\n"
                         "Enter your username: ")
        client = Client(sock, stop, username)
        client.start()
        client.join()


if __name__ == '__main__':
    main()
