import os
import struct
import time
import tqdm
import _functions as _f


class DataHandler_Client:

    def __init__(self) -> None:
        pass

    def send_command_to_server(self, sock, operating_system, dl_location,
                               username):  # pragma: no cover
        running = True
        while running:
            time.sleep(0.05)
            try:
                command = input(f"\nUsername: {username}\n"
                                f"Download location: {dl_location}\n"
                                "\nCOMMAND   | DESCRIPTION\n"
                                "---------------------------\n"
                                "remove    | Removes a file\n"
                                "download  | Download a file\n"
                                "upload    | Upload a file\n"
                                "file_size | Check file size\n"
                                "files     | Check available files\n\n"
                                "dl_local  | Update dl location\n"
                                "dc        | Disconnect\n"
                                "s_close   | Turns off the server\n\n"
                                "Enter command: ")
                if command == "dc":
                    sock.sendall(command.encode())
                    sock.close()
                    running = False
                    exit()
                elif command == "dl_local":
                    dl_location = _f.check_user_write_rights(
                        input("Enter new download location: "),
                        operating_system)
                elif command == "s_close":
                    print("Sending shutdown command to server.")
                    sock.sendall(command.encode())
                    sock.close()
                    running = False
                    exit()
                elif command == "upload" or command == "files" or command == "download":
                    sock.sendall(command.encode())
                elif command == "file_size" or command == "remove":
                    sock.sendall(command.encode())
                    filename = input("Enter filename: ")
                    sock.sendall(filename.encode())
                else:
                    input("You didn't enter a command.\n"
                          "Try again.\n"
                          "Press any key to continue.")
                    _f.clear_terminal(operating_system)
            except (OSError, KeyboardInterrupt, ValueError):
                break

    def recieve_data(self, sock, data, dl_location,
                     operating_system):  # pragma: no cover
        if not data:
            return
        elif data == "download":
            self.client_download(sock, dl_location)
        elif data == "upload":
            self.client_upload(sock)
        elif data == "broadcast":
            data = sock.recv(1024).decode()
            print(data)
        else:
            _f.clear_terminal(operating_system)
            data = sock.recv(1024).decode()
            print(data)
            input("Press any key to continue.")

    def filesize_and_pack_client(self):
        file_path = _f.get_file_path()
        filename = os.path.basename(file_path)
        filesize = os.path.getsize(file_path)
        struct_to_send = struct.pack("<Q", filesize)
        return file_path, filename, filesize, struct_to_send

    def client_download(self, sock, dl_location):  # pragma: no cover
        filename = _f.get_file_name()
        sock.sendall(filename.encode())
        filesize = Shared().recieve_file_size(sock)
        if filesize is None:
            return
        else:
            progress = tqdm.tqdm(range(filesize),
                                 f"Recieving {filename}",
                                 unit="B",
                                 unit_scale=True,
                                 unit_divisor=1024)
            with open(f"{dl_location}{filename}", "wb") as f:
                Shared().progress_bar(sock, filesize, progress, f)
                f.close()
            time.sleep(1)
            print(f"\nFile '{filename}' has been recieved.")

    def client_upload(self, sock):  # pragma: no cover
        try:
            file_path, filename, filesize, struct_test = self.filesize_and_pack_client(
            )
            sock.sendall(filename.encode())
            time.sleep(0.05)
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
            print("\nThe file does not exist.")
            sock.send(" ".encode())


class DataHandler_Server:

    def __init__(self) -> None:
        pass

    def send_data_to_client(self, conn, clients, data):  # pragma: no cover
        if data is None:
            return
        elif type(data) == list:
            data_str = str(data)
            conn.send(data_str.encode())
        elif data == "error":
            pass
        elif data.startswith("\nNew"):
            for conn in clients:
                conn.send("broadcast".encode())
                time.sleep(1)
                conn.send(data.encode())
        elif data.startswith("\nDuplicate"):
            print(data)
        else:
            conn.send(data.encode())

    def apply_command_server(self, sock, conn, data, username,
                             DATA_FOLDER):  # pragma: no cover
        if data == "files":
            print(f"\nRecieved command 'files' from: {username}.")
            conn.sendall("files".encode())
            all_files = _f.files_on_serv()
            return all_files
        elif data == "dc":
            conn.close()
        elif data == "s_close":
            print("Recieved command 's_close'. Shutting down the server.")
            # conn.close()
            sock.close()
            running = False
            return running
        elif data == "remove":
            file = conn.recv(1024).decode()
            conn.sendall("remove".encode())
            print(f"\nRecieved command 'remove' from user: {username}.")
            removed = _f.remove_file(file, DATA_FOLDER)
            return removed
        elif data == "download":
            print(f"\nRecieved command 'download' from user: {username}.")
            self.server_upload(conn, DATA_FOLDER)
        elif data == "upload":
            conn.sendall("upload".encode())
            print(f"\nRecieved command 'upload' from user: {username}.")
            return self.server_download(conn, username, DATA_FOLDER)
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

    def filesize_and_pack_server(self, DATA_FOLDER, filename):
        filesize = os.path.getsize(f"{DATA_FOLDER}{filename}")
        struct_to_send = struct.pack("<Q", filesize)
        return filesize, struct_to_send

    def server_download(self, conn, username, DATA_FOLDER):  # pragma: no cover
        files = _f.files_on_serv()
        filename = conn.recv(1024).decode()
        if filename == " ":
            print("User made some mistake. Aborting upload.")
            return "error"
        else:
            filesize = Shared().recieve_file_size(conn)
            progress = tqdm.tqdm(range(filesize),
                                 f"Recieving {filename} from user: {username}",
                                 unit="B",
                                 unit_scale=True,
                                 unit_divisor=1024)
            with open(f"{DATA_FOLDER}{filename}", "wb") as f:
                Shared().progress_bar(conn, filesize, progress, f)
                f.close()
            print(
                f"\nFile '{filename}' has been recieved from user: {username}."
            )
            return self.broadcast_new_file(username, filename, files)

    def server_upload(self, conn, DATA_FOLDER):  # pragma: no cover
        try:
            conn.sendall("download".encode())
            filename = conn.recv(1024).decode()
            filesize, struct_test = self.filesize_and_pack_server(
                DATA_FOLDER,
                filename,
            )
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
            return "Transfer complete"
        except FileNotFoundError:
            print("The file does not exist.")
            print("Aborting download")
            conn.send(" ".encode())

    def broadcast_new_file(self, username, filename, curr_files):
        if filename not in curr_files:
            print("Broadcasting the server got a new file.")
            return f"\nNew file '{filename}' uploaded by user '{username}'"
        else:
            return "\nDuplicate file. Not broadcasting."


class Shared:

    def __init__(self) -> None:
        pass

    def get_bytes(self):
        fmt = "<Q"
        expected_bytes = struct.calcsize(fmt)
        recieved_bytes = 0
        stream = bytes()
        return fmt, expected_bytes, recieved_bytes, stream

    def recieve_file_size(self, conn):  # pragma: no cover
        fmt, expected_bytes, recieved_bytes, stream = self.get_bytes()
        while recieved_bytes < expected_bytes:
            chunk = conn.recv(expected_bytes - recieved_bytes)
            if chunk == b' ':
                print(
                    "\nYou made a mistake. Most likely you entered a filename for a file"
                    " that doesnt exist on the server.Therefore is download aborted"
                    "\nEnter new command: ")
                return
            else:
                stream += chunk
                recieved_bytes += len(chunk)
                filesize = struct.unpack(fmt, stream)[0]
                return filesize

    def progress_bar(self, sock, filesize, progress, f):  # pragma: no cover
        recieved_bytes = 0
        while recieved_bytes < filesize:
            chunk = sock.recv(1024)
            if chunk:
                f.write(chunk)
                recieved_bytes += len(chunk)
                progress.update(len(chunk))
