import threading
import socket
import os
from time import sleep
from _datahandler import DataHandler


class Client(threading.Thread):

    def __init__(self, sock, stop, username, threads):
        threading.Thread.__init__(self)
        self.sock = sock
        self.stop = stop
        self.username = username
        self.threads = threads

    def run(self):
        self.sock.sendall(self.username.encode())
        print(self.sock.recv(8192).decode())
        self.threads.append(
            f"{self.name}:{socket.gethostbyname(socket.gethostname())}")
        threading.Thread(target=self.menu,
                         args=(
                             self.sock,
                             self.stop,
                             self.threads,
                             self.username,
                         )).start()
        while not self.stop.is_set():
            self.recieve_data(self.sock, self.stop)
            print(">> ")

    def menu(self, sock, stop, threads, username):
        threads.append(self.name)
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
                    threads.remove(self.name)
                    break
                elif command == "upload":
                    ul_thread = threading.Thread(target=DataHandler().upload,
                                                 args=(sock, command))
                    ul_thread.start()
                elif command == "file_size" or command == "remove":
                    sock.sendall(command.encode())
                    filename = input("Enter filename: ")
                    sock.sendall(filename.encode())
                elif command == "download":
                    sock.sendall(command.encode())
                    filename = input("Enter filename: ")
                    download_location = input("Enter download location: ")
                    dl_thread = threading.Thread(
                        target=DataHandler().client_recieve,
                        args=(sock, filename, download_location),
                        daemon=True)
                    dl_thread.start()
                    dl_thread.join()
                else:
                    sock.sendall(command.encode())
            except OSError as e:
                print(e)

    def recieve_data(self, sock, stop):
        data = sock.recv(8192).decode()
        if not data:
            return
        else:
            print(data)
        # input("Press any key to continue to main menu")


def main():  # pragma: no cover
    SERVER = '127.0.0.1'
    PORT = 44554
    stop = threading.Event()
    threads = []
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
        client = Client(sock, stop, username, threads)
        client.start()
        client.join()


if __name__ == '__main__':
    main()
