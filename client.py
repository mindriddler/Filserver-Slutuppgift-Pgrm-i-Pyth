import threading
import socket
import os
import platform
from _datahandler import DataHandler_Client


class Client(threading.Thread):

    def __init__(self, sock, stop):
        threading.Thread.__init__(self)
        self.sock = sock
        self.stop = stop
        self.username = input("Enter your username: ")
        self.operation_system = platform.platform()
        self.dl_location = input("Set your download location: ")
        self.menu = (f"\nUsername: {self.username}\n"
                     f"Download location: {self.dl_location}\n"
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

    def run(self):
        self.sock.sendall(self.username.encode())
        if "Windows" in self.operation_system:
            os.system("cls")
        else:
            os.system("clear")
        print(self.sock.recv(1024).decode())
        threading.Thread(target=DataHandler_Client().send_command_to_server,
                         args=(
                             self.sock,
                             self.stop,
                             self.menu,
                             self.operation_system,
                         )).start()
        while not self.stop.is_set():
            try:
                data = self.sock.recv(1024).decode()
                if not data:
                    break
                elif data == "dc":
                    print("You have disconnected from the server.")
                    break
                else:
                    DataHandler_Client().recieve_data(
                        self.sock,
                        data,
                        self.dl_location,
                    )
            except ConnectionAbortedError:
                print("You have disconnected from the server.")


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
