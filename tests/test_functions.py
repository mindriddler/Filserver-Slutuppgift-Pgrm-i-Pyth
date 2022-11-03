from App.server import Server


def test_files_on_serv():
    serv_init = Server(conn="", sock="", addr="", clients="")
    assert serv_init.files_on_serv() == [
        'Kiara.jpg', 'Anduin.jpg', 'file_for_testing_0B.txt'
    ]


def test_file_doesnt_exist():
    serv_init = Server(conn="", sock="", addr="", clients="")
    assert serv_init.remove_file(
        "file_for_testing_remov.txt"
    ) == "\n!!!File 'file_for_testing_remov.txt' does not exist!!!"


def test_check_file_size():
    serv_init = Server(conn="", sock="", addr="", clients="")
    assert serv_init.check_file_size(file="file_for_testing_0B.txt") == "0B"


def test_check_file_size_file_0B():
    serv_init = Server(conn="", sock="", addr="", clients="")
    assert serv_init.check_file_size(file="Anduin.jpg") == "3.29 MB"


def test_rm_file():
    open("Data/file_for_testing_remove.txt", "w")
    serv_init = Server(conn="", sock="", addr="", clients="")
    assert serv_init.remove_file(
        "file_for_testing_remove.txt"
    ) == "\nFile 'file_for_testing_remove.txt' has been removed."
