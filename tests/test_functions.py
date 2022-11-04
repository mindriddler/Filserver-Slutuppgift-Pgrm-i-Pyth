from App._functions import check_file_size, files_on_serv, remove_file
import os


def test_files_on_serv():
    files = [f for f in os.listdir("Data")]
    assert files_on_serv() == files


def test_file_doesnt_exist():
    assert remove_file(
        "file_for_testing_remov.txt"
    ) == "\n!!!File 'file_for_testing_remov.txt' does not exist!!!"


def test_check_file_size():
    assert check_file_size(file="file_for_testing_0B.txt") == "0B"


def test_check_file_size_file_0B():
    assert check_file_size(file="Anduin.jpg") == "3.29 MB"


def test_rm_file():
    open("Data/file_for_testing_remove.txt", "w")
    assert remove_file(
        "file_for_testing_remove.txt"
    ) == "\nFile 'file_for_testing_remove.txt' has been removed."
