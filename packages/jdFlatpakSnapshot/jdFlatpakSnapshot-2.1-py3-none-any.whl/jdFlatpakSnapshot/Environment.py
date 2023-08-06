from .SnapshotCollection import	SnapshotCollection
from .FlatpakHandler import FlatpakHandler
from .Settings import Settings
from PyQt6.QtGui import QIcon
from pathlib import Path
import json
import sys
import os


class Environment:
    def __init__(self):
        self.program_dir = os.path.dirname(os.path.realpath(__file__))
        self.data_dir = self._get_data_path()

        with open(os.path.join(self.program_dir, "version.txt"), "r", encoding="utf-8") as f:
            self.version = f.read().strip()

        self.icon = QIcon(os.path.join(self.program_dir, "icons", "app-icon.svg"))

        try:
            os.makedirs(self.data_dir)
        except FileExistsError:
            pass

        self.snapshot_collection = SnapshotCollection(self)
        self.snapshot_collection.load_snapshots()

        self.settings = Settings()
        self.settings.load(os.path.join(self.data_dir, "settings.json"))

        self.flatpak_handler = FlatpakHandler(self)

    def _get_data_path(self) -> str:
        if os.getenv("XDG_DATA_HOME"):
            return os.path.join(os.getenv("XDG_DATA_HOME"), "JakobDev", "jdFlatpakSnapshot")
        else:
            return os.path.join(str(Path.home()), ".local", "share", "JakobDev", "jdFlatpakSnapshot")
