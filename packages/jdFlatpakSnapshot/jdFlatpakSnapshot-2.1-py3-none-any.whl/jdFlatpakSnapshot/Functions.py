from .Constants import FLATPAK_DIRS, DEFAULT_DATETIME_FORMAT
from typing import Optional, Any, TYPE_CHECKING
from PyQt6.QtWidgets import QComboBox
import subprocess
import datetime
import zipfile
import uuid
import os


if TYPE_CHECKING:
    from .Environment import Environment


def list_files_recursive(path: str, start_path: str = "") -> list[str]:
    file_list = []
    for i in os.listdir(path):
        full_path = os.path.join(path, i)
        if os.path.isfile(full_path):
            file_list.append(os.path.join(start_path, i))
        elif os.path.isdir(full_path):
            file_list += list_files_recursive(full_path, os.path.join(start_path, i))
    return file_list


def human_readable_size(size: int) -> str:
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(size) < 1024.0:
            return f"{size:3.1f}{unit}B"
        size /= 1024.0
    return f"{size:.1f}YiB"


def format_datetime(dt: datetime.datetime, format: str) -> str:
    """
    Formats a datetime in the Format selected by the User
    """
    try:
        return dt.strftime(format)
    except ValueError:
        return dt.strftime(DEFAULT_DATETIME_FORMAT)



def select_combo_box_data(box: QComboBox, data: Any, default_index: int = 0) -> None:
    """
    Set the index to the item with the given data
    """
    index = box.findData(data)
    if index == -1:
        box.setCurrentIndex(default_index)
    else:
        box.setCurrentIndex(index)


def extract_file_from_zip(handler: zipfile.ZipFile, zip_path: str, extract_path: str) -> None:
    """
    Extract a file from a zip handler into the given path
    """
    try:
        os.makedirs(os.path.dirname(extract_path))
    except Exception:
        pass

    with handler.open(zip_path, "r") as f:
        with open(extract_path, "wb") as w:
            w.write(f.read())


def is_flatpak_installed(app_id: str) -> bool:
    """
    Checks if the given Flatpak is installed
    """
    for i in FLATPAK_DIRS:
        if os.path.isdir(os.path.join(i, "app", app_id)):
            return True
    return False


def is_run_as_flatpak() -> bool:
    """
    Checks if the App is run as Flatpak
    """
    return os.path.isfile("/.flatpak-info")
