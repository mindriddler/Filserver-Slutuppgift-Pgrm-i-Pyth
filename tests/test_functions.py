from os import listdir
from unittest import mock

import _functions

DATA_FOLDER = "Data/"  # Linux, uncomment to use
# DATA_FOLDER = "Data\\"  # Windows, uncomment to use


@mock.patch("platform.platform",
            side_effect=["Linux", "Windows", "Darwin", "else"])
def test_check_os_linux(mocked_os):
    assert _functions.check_os() == "Linux"
    assert _functions.check_os() == "Windows"
    assert _functions.check_os() == "OSX"
    assert _functions.check_os() == "else"


def test_files_on_serv():
    files = [f for f in listdir("Data")]
    assert _functions.files_on_serv() == files


def test_file_doesnt_exist():
    assert (_functions.remove_file("file_for_testing_remov.txt", DATA_FOLDER)
            == "\n!!!File 'file_for_testing_remov.txt' does not exist!!!")


def test_check_file_size_0B():
    assert _functions.check_file_size("file_for_testing_0B.txt",
                                      DATA_FOLDER) == "0B"


# i need to set or because for some reason windows and linux sets the filesize differently
def test_check_file_size_B():
    assert _functions.check_file_size("bytes.txt",
                                      DATA_FOLDER) == "18.0 B" or "17.0 B"


def test_check_file_size_KB():
    assert _functions.check_file_size("KB.txt",
                                      DATA_FOLDER) == "1.54 KB" or "1.46 KB"


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
    assert _functions.get_file_name() == "test.txt"
