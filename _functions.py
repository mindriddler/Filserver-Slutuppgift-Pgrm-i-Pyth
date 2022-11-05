import math
import os
import os.path
from _datahandler import DataHandler as dh


def apply_command(sock, conn, data, username, DATA_FOLDER,
                  clients):  # pragma: no cover
    if data == "files":
        print(f"\nRecieved command 'files' from: {username}.")
        conn.sendall("files".encode())
        all_files = files_on_serv()
        return all_files
    elif data == "dc":
        conn.close()
    elif data == "remove":
        file = conn.recv(1024).decode()
        print(f"\nRecieved command 'remove' from user: {username}.")
        removed = remove_file(file, DATA_FOLDER)
        return removed
    elif data == "download":
        print(f"\nRecieved command 'download' from user: {username}.")
        dh().upload_to_client(conn, DATA_FOLDER)
    elif data == "upload":
        print(f"\nRecieved command 'upload' from user: {username}.")
        dh().server_recieve(conn, username, DATA_FOLDER, clients)
    elif data == "file_size":
        try:
            file = conn.recv(1024).decode()
            print(f"\nRecieved command 'file_size' from user: {username}.")
            file_size = f"File size of '{file}' is: {check_file_size(file, DATA_FOLDER)}"
            return file_size
        except OSError:
            data = "!!!That file does not exist!!!"
            print(data)
            return data


def check_file_size(file, DATA_FOLDER):
    # https://stackoverflow.com/questions/5194057/better-way-to-convert-file-sizes-in-python
    file_size = os.path.getsize(f"{DATA_FOLDER}{file}")
    if file_size == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB")
    i = int(math.floor(math.log(file_size, 1024)))
    p = math.pow(1024, i)
    s = round(file_size / p, 2)
    return "%s %s" % (s, size_name[i])


def files_on_serv():
    files = [f for f in os.listdir("Data")]
    return files


def remove_file(file, DATA_FOLDER):
    try:
        os.remove(f"{DATA_FOLDER}{file}")
        data = f"\nFile '{file}' has been removed."
        print(data)
        return data
    except OSError:
        data = f"\n!!!File '{file}' does not exist!!!"
        print(data)
        return data
