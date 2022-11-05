import struct
import tqdm
from os import listdir
import os.path


class DataHandler:  # pragma: no cover

    def recieve_file_size(self, conn):
        fmt = "<Q"
        expected_bytes = struct.calcsize(fmt)
        recieved_bytes = 0
        stream = bytes()
        while recieved_bytes < expected_bytes:
            chunk = conn.recv(expected_bytes - recieved_bytes)
            stream += chunk
            recieved_bytes += len(chunk)
        filesize = struct.unpack(fmt, stream)[0]
        return filesize

    def client_recieve(self, sock, filename, download_location):
        try:
            sock.sendall(filename.encode())
            filesize = self.recieve_file_size(sock)
            progress = tqdm.tqdm(range(filesize),
                                 f"Recieving {filename}",
                                 unit="B",
                                 unit_scale=True,
                                 unit_divisor=1024,
                                 disable=False)
            with open(f"{download_location}{filename}", "wb") as f:
                recieved_bytes = 0
                while recieved_bytes < filesize:
                    chunk = sock.recv(1024)
                    if chunk:
                        f.write(chunk)
                        recieved_bytes += len(chunk)
                        progress.update(len(chunk))
                f.close()
            print(f"\nFile '{filename}' has been recieved.")
        except AttributeError:
            pass

    def server_recieve(self, conn, username, DATA_FOLDER, clients):
        curr_files = [f for f in listdir(DATA_FOLDER)]
        filename = conn.recv(1024).decode()
        filesize = self.recieve_file_size(conn)
        progress = tqdm.tqdm(range(filesize),
                             f"Recieving {filename} from user: {username}",
                             unit="B",
                             unit_scale=True,
                             unit_divisor=1024)
        with open(f"{DATA_FOLDER}{filename}", "wb") as f:
            recieved_bytes = 0
            while recieved_bytes < filesize:
                chunk = conn.recv(1024)
                if chunk:
                    f.write(chunk)
                    recieved_bytes += len(chunk)
                    progress.update(len(chunk))
            f.close()
        print(f"\nFile '{filename}' has been recieved from user: {username}.")
        self.broadcast_new_file(conn, username, clients, filename, curr_files)

    def upload_to_client(self, conn, DATA_FOLDER):
        filename = conn.recv(1024).decode()
        filesize = os.path.getsize(f"{DATA_FOLDER}{filename}")
        struct_test = struct.pack("<Q", filesize)
        conn.sendall(struct_test)
        progress = tqdm.tqdm(range(filesize),
                             f"Uploading {filename}",
                             unit="B",
                             unit_scale=True,
                             unit_divisor=1024)
        with open(f"{DATA_FOLDER}{filename}", "rb") as f:
            while read_bytes := f.read(1024):
                conn.sendall(read_bytes)
                progress.update(len(read_bytes))
            f.close()
        conn.send("Transfer complete".encode())
        return "Transfer complete"

    def upload(self, sock, command):
        try:
            sock.sendall(command.encode())
            file_path = input("File path: ")
            filename = os.path.basename(file_path)
            sock.sendall(filename.encode())
            filesize = os.path.getsize(file_path)
            struct_test = struct.pack("<Q", filesize)
            sock.sendall(struct_test)
            progress = tqdm.tqdm(range(filesize),
                                 f"Uploading {filename}",
                                 unit="B",
                                 unit_scale=True,
                                 unit_divisor=1024)
            with open(file_path, "rb") as f:
                while read_bytes := f.read(1024):
                    sock.sendall(read_bytes)
                    progress.update(len(read_bytes))
                f.close()
            return "Transfer complete"
        except FileNotFoundError:
            print("The file does not exist.")

    def broadcast_new_file(self, conn, username, clients, filename,
                           curr_files):
        new_file_uploaded = f"\nNew file '{filename}' uploaded by user '{username}'"

        if filename not in curr_files:
            for conn in clients:
                conn.sendall(new_file_uploaded.encode())
        else:
            print("\nDuplicate file. Not broadcasting.")
