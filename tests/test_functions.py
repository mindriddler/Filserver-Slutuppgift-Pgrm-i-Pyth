from os import listdir
from unittest import mock
from _datahandler import DataHandler_Client, DataHandler_Server, Shared
import _functions

# DATA_FOLDER = "Data/"  # Linux, uncomment to use
DATA_FOLDER = "Data\\"  # Windows, uncomment to use


def test_files_on_serv():
    files = [f for f in listdir("Data")]
    assert _functions.files_on_serv() == files


def test_file_doesnt_exist():
    assert (_functions.remove_file("file_for_testing_remov.txt", DATA_FOLDER)
            == "\n!!!File 'file_for_testing_remov.txt' does not exist!!!")


def test_check_file_size_0B():
    assert _functions.check_file_size("file_for_testing_0B.txt",
                                      DATA_FOLDER) == "0B"


def test_check_file_size_B():
    assert _functions.check_file_size("bytes.txt", DATA_FOLDER) == "18.0 B"


def test_check_file_size_KB():
    assert _functions.check_file_size("KB.txt", DATA_FOLDER) == "1.54 KB"


def test_check_file_size_MB():
    assert _functions.check_file_size("Anduin.jpg", DATA_FOLDER) == "3.29 MB"


# Cant push +1 GB to github :D
# def test_check_file_size_GB():
#     assert _functions.check_file_size("GB.mkv", DATA_FOLDER) == "3.69 GB"


def test_rm_file():
    open("Data/file_for_testing_remove.txt", "w")
    assert (_functions.remove_file("file_for_testing_remove.txt", DATA_FOLDER)
            == "\nFile 'file_for_testing_remove.txt' has been removed.")


@mock.patch("builtins.input", return_value="test.txt")
def test_get_file_name(mock_input):
    # with mock.patch.object(builtins, "input", lambda _: "test.txt"):
    assert _functions.get_file_name() == "test.txt"


@mock.patch("builtins.input", return_value="/home/mindriddler/Skrivbord/test/")
def test_get_file_path(mocked_input):
    assert _functions.get_file_path() == "/home/mindriddler/Skrivbord/test/"


@mock.patch.object(_functions, "get_file_path", return_value="Data\\Kiara.jpg")
def test_filesize_and_pack_client(mocked_file_path):
    class_init = DataHandler_Client()
    assert class_init.filesize_and_pack_client() == (
        'Data\\Kiara.jpg', 'Kiara.jpg', 3678528, b'@!8\x00\x00\x00\x00\x00')


def test_filesize_and_pack_server():
    class_init = DataHandler_Server()
    assert class_init.filesize_and_pack_server(
        DATA_FOLDER, "Kiara.jpg") == (3678528, b'@!8\x00\x00\x00\x00\x00')


def test_get_bytes():
    class_init = Shared()
    assert class_init.get_bytes() == ('<Q', 8, 0, b'')


def test_broadcast():
    class_init = DataHandler_Server()
    assert class_init.broadcast_new_file(
        username="Test_user",
        filename="test_file.txt",
        curr_files=[],
    ) == "\nNew file 'test_file.txt' uploaded by user 'Test_user'"


def test_broadcast_duplicate_file():
    class_init = DataHandler_Server()
    assert class_init.broadcast_new_file(
        username="Test_user",
        filename="file_for_duplicate_broadcast_test.txt",
        curr_files=["file_for_duplicate_broadcast_test.txt"
                    ]) == "\nDuplicate file. Not broadcasting."
