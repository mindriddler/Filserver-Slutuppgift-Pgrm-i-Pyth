import math
import os
import os.path
import platform


def check_file_size(file, DATA_FOLDER):
    # https://stackoverflow.com/questions/5194057/better-way-to-convert-file-sizes-in-python
    file_size = os.path.getsize(f"{DATA_FOLDER}{file}")
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


def remove_file(file, DATA_FOLDER):
    try:
        os.remove(f"{DATA_FOLDER}{file}")
        data = f"\nFile '{file}' has been removed."
        print(data)
        return data
    except OSError:
        data = f"\n!!!File '{file}' does not exist!!!"
        print(data)
        return data


def get_file_name():
    filename = input("Enter filename: ")
    return filename


def get_file_path():
    file_path = input("File path: ")
    return file_path


def check_os():
    operating_system = platform.platform()
    if "Windows" in operating_system:
        operating_system = "Windows"
        return operating_system
    else:
        operating_system = "Unix"
        return operating_system


def check_user_write_rights(dl_location, operating_system):
    write_right = False

    while not write_right:
        dl_location = check_backslash(dl_location, operating_system)
        if operating_system == "Windows":
            try:
                open(f"{dl_location}testfile.txt", "w")
                write_right = True
            except Exception:
                dl_location = input(
                    "You do not have write rights to this folder.\n"
                    "Enter a new download location: ")
        else:
            try:
                open(f"{dl_location}testfile.txt", "w")
                write_right = True
            except Exception:
                dl_location = input(
                    "You do not have write rights to this folder.\n"
                    "Enter a new download location: ")

    os.remove(f"{dl_location}testfile.txt")
    dl_location = check_backslash(dl_location, operating_system)
    return dl_location


def check_backslash(dl_location, operating_system):
    if "Windows" in operating_system:
        if dl_location.endswith("\\") is False:
            return f"{dl_location}\\"
        else:
            return dl_location
    else:
        if dl_location.endswith("/") is False:
            return f"{dl_location}/"
        else:
            return dl_location


# def check_if_dir_exist(dl_location, operating_system):
#     while True:
#         if not os.path.exists(dl_location):
#             choice = input(
#                 "The folder does not exist.\n"
#                 "Do you want me to create it for you? [Yes or no]: ").lower()
#             if choice == "yes":
#                 os.mkdir(dl_location)
#                 if operating_system == "Windows":
#                     return f"{dl_location}\\"
#                 else:
#                     return f"{dl_location}/"
#             elif choice == "no":
#                 dl_location = input("Enter a new download location: ")
#                 if operating_system == "Windows" and dl_location.endswith(
#                         "\\") is False:
#                     return f"{dl_location}\\"
#                 elif dl_location.endswith("/") is False:
#                     return f"{dl_location}/"
#                 else:
#                     return dl_location
