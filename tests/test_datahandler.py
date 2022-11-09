from unittest import mock
import _functions
from _datahandler import DataHandler_Client, DataHandler_Server, Shared

DATA_FOLDER = "Data/"  # Linux, uncomment to use
# DATA_FOLDER = "Data\\"  # Windows, uncomment to use


@mock.patch.object(_functions,
                   "get_file_path",
                   return_value=f"{DATA_FOLDER}Kiara.jpg")
def test_filesize_and_pack_client(mocked_file_path):
    class_init = DataHandler_Client()
    assert class_init.filesize_and_pack_client() == (
        f"{DATA_FOLDER}Kiara.jpg", 'Kiara.jpg', 3678528,
        b'@!8\x00\x00\x00\x00\x00')


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
