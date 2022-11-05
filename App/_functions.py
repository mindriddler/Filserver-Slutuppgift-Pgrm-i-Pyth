import math
import os
import os.path
import struct
import tqdm


def apply_command(conn, data, username, DATA_FOLDER,
                  clients):  # pragma: no cover
    if data == "files":
        print(f"\nRecieved command '/files' from: {username}.")
        all_files = files_on_serv()
        send_to_client(conn, all_files)
    elif data == "dc":
        conn.close()
    elif data == "remove":
        file = input("Enter filename: ")
        print(f"\nRecieved command 'remove' from user: {username}.")
        removed = remove_file(file)
        send_to_client(conn, removed, DATA_FOLDER)
    elif data == "dwnl":
        pass
    elif "upload" in data:
        print(f"\nRecieved command 'upload' from user: {username}.")
        upload(conn, username, DATA_FOLDER, clients)
    elif data == "file_size":
        try:
            file = input("Enter filename: ")
            print(f"\nRecieved command 'file_size' from user: {username}.")
            file_size = f"File size of '{file}' is: {check_file_size(file, DATA_FOLDER)}"
            send_to_client(conn, file_size)
        except OSError:
            data = "!!!That file does not exist!!!"
            print(data)
            send_to_client(conn, data)


def send_to_client(conn, data):  # pragma: no cover
    if type(data) == list:
        data_str = str(data)
        conn.send(data_str.encode())
    else:
        conn.send(data.encode())


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


def recieve_file_size(conn):
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


def upload(conn, username, DATA_FOLDER, clients):
    curr_files = [f for f in os.listdir(DATA_FOLDER)]
    filename = conn.recv(1024).decode()
    filesize = recieve_file_size(conn)
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
    broadcast_new_file(conn, username, clients, filename, curr_files)


def download(data):
    pass


def broadcast_new_file(conn, username, clients, filename, curr_files):
    new_file_uploaded = f"\nNew file '{filename}' uploaded by user '{username}'"

    if filename not in curr_files:
        for conn in clients:
            conn.sendall(new_file_uploaded.encode())
    else:
        print("\nDuplicate file. Not broadcasting.")
