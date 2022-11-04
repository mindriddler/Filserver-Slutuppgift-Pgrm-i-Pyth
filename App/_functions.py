import math
import os
import os.path
import struct
import tqdm


def apply_command(conn, data, username, SEPARATOR,
                  BUFFER_SIZE):  # pragma: no cover
    if "/files" in data:
        print(f"\nRecieved command '/files' from{username}. "
              "They want to know what files we have.")
        all_files = files_on_serv()
        print(f"\nThe files we have are the following: {all_files}")
        send_to_client(conn, all_files)
    elif data == "dc":
        conn.close()
    elif "rm" in data:
        file = "".join(data.split(" ")[1:])
        print(f"\nRecieved command 'rm' from{username}. "
              f"They want to remove the file {file}.")
        removed = remove_file(file)
        send_to_client(conn, removed)
    elif data == "dwnl":
        pass
    elif "upld" in data:
        upload(conn, data, SEPARATOR, BUFFER_SIZE)
    elif "/fs" in data:
        try:
            file = "".join(data.split(" ")[1:])
            print(f"\nRecieved command '/fs' from{username}. "
                  f"They want to know what the file size of '{file}' is.")
            file_size = f"File size of '{file}' is: {check_file_size(file)}"
            print(f"\n{file_size}")
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


def check_file_size(file):
    # https://stackoverflow.com/questions/5194057/better-way-to-convert-file-sizes-in-python
    file_size = os.path.getsize(f"Data\{file}")
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


def remove_file(file):
    try:
        os.remove(f"Data/{file}")
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


def recieve_file(conn, filename):
    filesize = recieve_file_size(conn)
    with open(f"Data\{filename}", "wb") as f:
        recieved_bytes = 0
        while recieved_bytes < filesize:
            chunk = conn.recv(1024)
            if chunk:
                f.write(chunk)
                recieved_bytes += len(chunk)
        f.close()
        print("Transfer completed")


def upload(conn, data, SEPARATOR, BUFFER_SIZE):
    file_path = conn.recv(1024).decode()
    file_name = file_path
    recieve_file(conn, file_name)


def download(data):
    pass


# def broadcast_new_file(self, conn, clients):
#     print("thread started")
#     file_list = [f for f in os.listdir("Data")]
#     while True:
#         files = os.listdir("Data")
#         paths = [os.path.join("Data", basename) for basename in files]
#         newest_file = max(paths, key=os.path.getctime)
#         for conn in clients:
#             conn.send(
#                 f"New file has been added to the server: '{newest_file}'".
#                 encode()
