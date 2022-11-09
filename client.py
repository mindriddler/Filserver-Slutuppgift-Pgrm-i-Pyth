import threading
import socket
from _datahandler import DataHandler_Client
import _functions


class Client(threading.Thread):

    def __init__(self, sock, stop):
        threading.Thread.__init__(self)
        self.sock = sock
        self.stop = stop
        self.username = input("Enter your username: ")
        self.operating_system = _functions.check_os()
        self.dl_location = input("Set your download location: ")

    def run(self):
        self.sock.sendall(self.username.encode())
        self.dl_location = _functions.check_user_write_rights(
            self.dl_location, self.operating_system)
        _functions.clear_terminal(self.operating_system)
        print(self.sock.recv(1024).decode())
        threading.Thread(target=DataHandler_Client().send_command_to_server,
                         args=(
                             self.sock,
                             self.operating_system,
                             self.dl_location,
                             self.username,
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
                        self.operating_system,
                    )
            except ConnectionAbortedError:
                print("You have disconnected from the server.")
            except OSError:
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
