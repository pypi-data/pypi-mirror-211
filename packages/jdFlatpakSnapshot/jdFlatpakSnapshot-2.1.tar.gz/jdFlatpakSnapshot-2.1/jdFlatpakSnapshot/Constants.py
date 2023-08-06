from PyQt6.QtCore import QCoreApplication
import collections
import os

FLATPAK_DIRS = (
    "/var/lib/flatpak",
    os.path.expanduser("~/.local/share/flatpak")
)

CompressionTuple = collections.namedtuple("compression_tuple", ("name", "mode", "suffix"))
COMPRESSION_METHODS = (
    CompressionTuple(QCoreApplication.translate("Constants", "None"), "", ""),
    CompressionTuple("GZIP", "gz", ".gz"),
    CompressionTuple("BZIP2", "bz2", ".bz2"),
    CompressionTuple("LZMA", "xz", ".xz")
)

DEFAULT_DATETIME_FORMAT = "%Y-%m-%d %H:%M"
