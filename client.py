import threading
import socket
import os
import platform
from time import sleep
from _datahandler import DataHandler


class Client(threading.Thread):

    def __init__(self, sock, stop):
        threading.Thread.__init__(self)
        self.sock = sock
        self.stop = stop
        self.username = input("Enter your username: ")
        self.operation_system = platform.platform()
        self.dl_location = input("Set your download location: ")

    def run(self):
        self.sock.sendall(self.username.encode())
        if "Windows" in self.operation_system:
            os.system("cls")
        else:
            os.system("clear")
        print(self.sock.recv(1024).decode())
        threading.Thread(target=self.menu,
                         args=(self.sock, self.stop, self.username,
                               self.dl_location)).start()
        while not self.stop.is_set():
            try:
                data = self.sock.recv(1024).decode()
                if not data:
                    break
                else:
                    DataHandler().recieve_data(self.sock, data,
                                               self.dl_location)
            except ConnectionAbortedError:
                print("You have disconnected from the server.")

    def menu(self, sock, stop, username, dl_location):
        while not stop.is_set():
            try:
                sleep(0.05)
                # input("Press any key to continue")
                command = input(f"\nUsername: {username}\n"
                                f"Download location: {dl_location}\n"
                                "\nCOMMAND   | DESCRIPTION\n"
                                "---------------------------\n"
                                "remove    | Removes a file\n"
                                "download  | Upload a file\n"
                                "upload    | Download a file\n"
                                "file_size | Check file size\n"
                                "files     | Check available files\n\n"
                                "dl_local  | Update dl location\n"
                                "dc        | Disconnect\n\n"
                                "Enter command: ")
                if command == "dc":
                    sock.sendall(command.encode())
                    sock.close()
                    stop.set()
                    break
                elif command == "dl_local":
                    self.dl_location = input("New download location: ")
                elif command == "upload":
                    sock.sendall(command.encode())
                elif command == "file_size" or command == "remove":
                    sock.sendall(command.encode())
                    filename = input("Enter filename: ")
                    sock.sendall(filename.encode())
                elif command == "files":
                    sock.sendall(command.encode())
                elif command == "download":
                    sock.sendall(command.encode())
                else:
                    input(
                        "You didn't enter a command.\nTry again.\nPress any key to continue."
                    )
                    if "Windows" in self.operation_system:
                        os.system("cls")
                    else:
                        os.system("clear")
            except OSError as e:
                print(e)
                break


def main():
    SERVER = "127.0.0.1"
    PORT = 44554
    stop = threading.Event()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        print("Connecting to server.\nPlease standby.")
        try:
            sock.connect((SERVER, PORT))
        except ConnectionRefusedError as e:
            input(f"{e}. Is the server running?\n\nPress any key to continue.")
            return
        print(f"\n\nConnect to {SERVER}:{PORT}\n")
        client = Client(sock, stop)
        client.start()
        client.join()


if __name__ == "__main__":
    main()
