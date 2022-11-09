from unittest import mock
from os import getlogin
import _functions

username = getlogin()


@mock.patch("builtins.input", return_value=f"/home/{username}/Skrivbord/test/")
def test_get_file_path(mocked_input):
    assert _functions.get_file_path() == f"/home/{username}/Skrivbord/test/"


@mock.patch("builtins.open", side_effect=[Exception, True])
@mock.patch("os.remove", return_value=True)
@mock.patch("builtins.input", return_value=f"/home/{username}/Skrivbord/")
def test_check_user_write_rights_False_linux(mocked_open, mocked_remove,
                                             mocked_input):
    assert _functions.check_user_write_rights(
        "/", operating_system="Linux") == f"/home/{username}/Skrivbord/"


@mock.patch("os.remove", return_value=True)
@mock.patch("builtins.open", return_value=True)
def test_check_user_write_rights_True_linux(mocked_open, mocked_remove):
    assert _functions.check_user_write_rights(
        f"/home/{username}/Skrivbord/",
        operating_system="Linux") == f"/home/{username}/Skrivbord/"


def test_check_backslash_linux():

    assert _functions.check_backslash(
        f"/home/{username}/Skrivbord",
        "Linux",
    ) == f"/home/{username}/Skrivbord/"
    assert _functions.check_backslash(
        f"/home/{username}/Skrivbord/",
        "Linux") == f"/home/{username}/Skrivbord/"
