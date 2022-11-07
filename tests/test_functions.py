from _functions import check_file_size, files_on_serv, remove_file
from os import listdir
from _datahandler import DataHandler
import socket

DATA_FOLDER = "Data/"  # Linux, uncomment to use
# DATA_FOLDER = "Data\\"  # Windows, uncomment to use


def test_files_on_serv():
    files = [f for f in listdir("Data")]
    assert files_on_serv() == files


def test_file_doesnt_exist():
    assert (remove_file("file_for_testing_remov.txt", DATA_FOLDER) ==
            "\n!!!File 'file_for_testing_remov.txt' does not exist!!!")


def test_check_file_size_0B():
    assert check_file_size("file_for_testing_0B.txt", DATA_FOLDER) == "0B"


def test_check_file_size_B():
    assert check_file_size("bytes.txt", DATA_FOLDER) == "17.0 B"


def test_check_file_size_KB():
    assert check_file_size("KB.pdf", DATA_FOLDER) == "195.5 KB"


def test_check_file_size_MB():
    assert check_file_size("Anduin.jpg", DATA_FOLDER) == "3.29 MB"


def test_check_file_size_GB():
    assert check_file_size("GB.mkv", DATA_FOLDER) == "3.69 GB"


def test_rm_file():
    open("Data/file_for_testing_remove.txt", "w")
    assert (remove_file("file_for_testing_remove.txt", DATA_FOLDER) ==
            "\nFile 'file_for_testing_remove.txt' has been removed.")


def test_broadcast():
    SERVER = '127.0.0.1'
    PORT = 44554
    files = [f for f in listdir("Data")]
    filename = "test_broadcast_file.txt"
    username = "test"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((SERVER, PORT))
        clients = []
        clients.append(sock)
        class_init = DataHandler()
        open(f"{DATA_FOLDER}test_broadcast_file.txt", "w")
        assert (class_init.broadcast_new_file(
            sock,
            username,
            clients,
            filename,
            files,
        ) == f"\nNew file '{filename}' uploaded by user '{username}'")
        remove_file(filename, DATA_FOLDER)
