from unittest import mock
from os import getlogin
import _functions

username = getlogin()


@mock.patch("builtins.input", return_value="/home/mindriddler/Skrivbord/test/")
def test_get_file_path(mocked_input):
    assert _functions.get_file_path() == "/home/mindriddler/Skrivbord/test/"


@mock.patch("_functions.check_user_write_rights", return_value=False)
@mock.patch("builtins.open", mock.mock_open)
@mock.patch("os.remove", return_value=True)
@mock.patch("builtins.input", return_value="/home/mindriddler/Skrivbord/")
def test_check_user_write_rights_False_linux(
    mocked_write_rights,
    mocked_open,
    mocked_input,
):
    assert _functions.check_user_write_rights(
        "/", operating_system="Linux") is False


@mock.patch("os.remove", return_value=True)
@mock.patch("builtins.open", return_value=True)
def test_check_user_write_rights_True_linux(mocked_open, mocked_remove):
    assert _functions.check_user_write_rights(
        "/home/mindriddler/Skrivbord/",
        operating_system="Linux") == "/home/mindriddler/Skrivbord/"


def test_check_backslash_linux():

    assert _functions.check_backslash(
        f"/home/{username}/Skrivbord",
        "Linux",
    ) == f"/home/{username}/Skrivbord/"
    assert _functions.check_backslash(
        f"/home/{username}/Skrivbord/",
        "Linux") == f"/home/{username}/Skrivbord/"


@mock.patch("platform.platform", return_value="Unix")
def test_check_os_mock(mocked_platform):
    assert _functions.check_os() == "Unix"
