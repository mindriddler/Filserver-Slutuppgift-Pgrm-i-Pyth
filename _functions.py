import math
import os
import os.path
from _datahandler import DataHandler





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
