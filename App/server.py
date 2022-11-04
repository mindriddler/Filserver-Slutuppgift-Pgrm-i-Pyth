import socket
import threading
import _functions as _f
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
                    _f.apply_command(
                        self.conn,
                        data,
                        username,
                        self.SEPARATOR,
                        self.BUFFER_SIZE,
                    )
            except OSError:
                print(
                    f"User:{username} running on {self.name} disconnected.\n")
                break


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
