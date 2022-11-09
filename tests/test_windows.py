from unittest import mock
from os import getlogin
import _functions

username = getlogin()


def test_check_os():
    assert _functions.check_os() == "Windows"


def test_check_user_write_rights_True_windows():
    assert _functions.check_user_write_rights(
        f"C:\\Users\\{username}\\Desktop\\",
        operating_system="Windows",
    ) == f"C:\\Users\\{username}\\Desktop\\"


@mock.patch("builtins.input", return_value=f"C:\\Users\\{username}\\Desktop\\")
def test_check_user_write_rights_False_windows(mocked_input):
    assert _functions.check_user_write_rights(
        "C:\\",
        operating_system="Windows") == f"C:\\Users\\{username}\\Desktop\\"
    # out, err = capfd.readouterr()
    # assert out == ""


def test_check_backslash_windows():
    assert _functions.check_backslash(
        f"C:\\Users\\{username}\\Desktop",
        "Windows") == f"C:\\Users\\{username}\\Desktop\\"
    assert _functions.check_backslash(
        f"C:\\Users\\{username}\\Desktop\\",
        "Windows") == f"C:\\Users\\{username}\\Desktop\\"
