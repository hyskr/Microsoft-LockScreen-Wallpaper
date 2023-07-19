import os
import re
import shutil
import hashlib
import logging
from datetime import datetime
from PIL import Image
import ctypes

BASE = os.path.expanduser("~")
BASEP = "." + ""
LOG_FILE = BASEP + "\\wallpaper_getter.log"
SOURCE_FOLDER = (
    BASE
    + "\\AppData\\Local\\Packages\\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\\LocalState\\Assets"
)
TARGET_FOLDER_PORTRAIT = BASEP + "\\微软壁纸 竖版"
TARGET_FOLDER_LANDSCAPE = BASEP + "\\微软壁纸 横版"

def setup_logger(log_file):
    """
    Setup logger
    :param log_file: log file path
    """
    logger = logging.getLogger("my_logger")
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s:%(levelname)s:%(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger

def hide_file(file_path):
    """
    Hide a file in windows.
    :param file_path: the full path of the file
    """
    FILE_ATTRIBUTE_HIDDEN = 0x02
    ret = ctypes.windll.kernel32.SetFileAttributesW(file_path, FILE_ATTRIBUTE_HIDDEN)
    if not ret:
        raise ctypes.WinError()

def get_file_hash(file_path):
    """
    Calculate the MD5 hash of a file.
    
    :param file_path: the full path of the file
    :return: the MD5 hash of the file
    """
    hasher = hashlib.md5()
    with open(file_path, "rb") as afile:
        buf = afile.read()
        hasher.update(buf)
    return hasher.hexdigest()


def extract_hashids(log_file):
    """
    Extract unique hashids from log file.
    
    :param log_file: log file path
    :return: a set of unique hashids
    """
    with open(log_file, "r") as file:
        log_content = file.read()
    hashids = re.findall(r"[a-fA-F\d]{32}", log_content)
    hashids = set(hashids)
    return hashids


def get_max_num(target_folder):
    """
    Get the maximum number from file names in the target folder.
    
    :param target_folder: the target folder path
    :return: the maximum number
    """
    max_num = 0
    for filename in target_folder:
        match = re.search(r"(\d{8})(\d+)", filename)
        if match:
            num = int(match.group(2))
            if num > max_num:
                max_num = num
    return max_num


def copy_files(source_folder, target_folder_landscape, target_folder_portrait, log_file=LOG_FILE):
    """
    Copy files from the source folder to the target folders.
    
    :param source_folder: the source folder path
    :param target_folder_landscape: the target folder path for landscape images
    :param target_folder_portrait: the target folder path for portrait images
    :param log_file: log file path
    """
    if not os.path.exists(source_folder):
        print("%r does not exist" % source_folder)
        logger.error("%r does not exist", source_folder)
        return

    if not os.path.exists(target_folder_landscape):
        os.makedirs(target_folder_landscape)
    if not os.path.exists(target_folder_portrait):
        os.makedirs(target_folder_portrait)

    unique_hashes = extract_hashids(log_file)

    source_files = os.listdir(source_folder)

    target_landscape_files = os.listdir(target_folder_landscape)
    target_portrait_files = os.listdir(target_folder_portrait)

    landscape_max_num = get_max_num(target_landscape_files)
    portrait_max_num = get_max_num(target_portrait_files)

    # Copy and rename the files
    landscape_i = landscape_max_num + 1
    portrait_i = portrait_max_num + 1

    for file in source_files:
        file_path = os.path.join(source_folder, file)
        file_hash = get_file_hash(file_path)
        if file_hash in unique_hashes:
            logger.info("%r already exists", file_hash)
            continue
        else:
            logger.info("%r added", file_hash)
        image = Image.open(file_path)
        width, height = image.size
        if width > height:
            shutil.copy(
                file_path,
                os.path.join(
                    target_folder_landscape,
                    datetime.now().strftime("%Y-%m-%d-") + str(landscape_i) + ".jpg",
                ),
            )
            landscape_i += 1
        else:
            shutil.copy(
                file_path,
                os.path.join(
                    target_folder_portrait,
                    datetime.now().strftime("%Y-%m-%d-") + str(portrait_i) + ".jpg",
                ),
            )
            portrait_i += 1

    # print(unique_hashes)



# input("Press Enter to exit...")
if __name__ == "__main__":
    if not os.path.exists(LOG_FILE):
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        open(LOG_FILE, "w").close()
        hide_file(LOG_FILE)
        print("log file created")
    else:
        print("log file exists")

    logger = setup_logger(LOG_FILE)

    copy_files(SOURCE_FOLDER, TARGET_FOLDER_LANDSCAPE, TARGET_FOLDER_PORTRAIT)